# 🧠 Docker Networking — From Zero to Real Communication (CLI-First Lab)

## Goal of this lab

By the end of this lab, you will be able to:

- Explain how Docker networking works internally
- Create and manage Docker networks from the CLI
- Make containers communicate with each other
- Debug networking problems using inspection tools
- Understand the difference between container networking and port mapping

- 🚫 No Docker Compose
- 🚫 No shortcuts
- ✅ Real understanding

## How to Use This Lab

This lab is interactive:

- You will read a small theory section
- Then immediately prove it using CLI commands
- You will observe, inspect, and explain what Docker did for you

Do not skip steps.

---

## PART 1 — The Foundation: How Docker Networking Works

### 1. Container Isolation (The “Private Apartment”)

When you run a Docker container, it does not live directly on your computer’s main network.

Each container gets its own network namespace.

This means:

- Its own network interfaces
- Its own IP address
- Its own routing table
- Its own firewall rules

Docker automatically sets all of this up for you.

#### 🧪 Exercise 1 — Prove Network Isolation

Run a container:

```sh
docker run -it alpine sh
```

Inside the container:

```sh
ip a
```

**✅ Observe**

- You see a network interface (usually eth0)
- You see an IP address (usually 172.x.x.x)

Exit the container:

```sh
exit
```

**🧠 Think**

- Does this interface exist on your host?
- Did you configure this IP manually?
- Who created this network setup?

Key idea: Docker created a private network environment for this container.

### 2. The Default Network: bridge (The Local Neighborhood)

If you don’t specify a network, Docker attaches containers to the default bridge network.

This bridge:

- Acts like a virtual router
- Gives containers private IPs
- Uses NAT so containers can reach the internet

#### 🧪 Exercise 2 — Inspect the Default Bridge

List networks:
```sh
docker network ls
```

You should see:

- bridge
- host
- none

Inspect the bridge:
```sh
docker network inspect bridge
```

**✅ Observe**

- The subnet (172.x.x.0/16)
- The "Containers" section

### 3. What Docker Did Automatically (Very Important)

At this point, Docker has already:

- Created a virtual network
- Assigned an IP
- Created routing rules
- Enabled outbound internet access (NAT)

You did none of this manually.

Mental rule:

Docker networking is Linux networking with automation.

---

## PART 2 — Why Containers Don’t Automatically Find Each Other

### 4. Containers Without DNS (Failure First)

Let’s run two containers without specifying a network.

#### 🧪 Exercise 3 — Create Two Containers

```sh
docker run -it --name c1 alpine sh
```

In another terminal:
```sh
docker run -it --name c2 alpine sh
```

Inside c2, try:
```sh
ping c1
```

**❌ Expected Result**

Ping fails.

Try:
```sh
ping 8.8.8.8
```

**✅ Works**

**🧠 Think**

- Internet works
- Container name does NOT resolve
- Why?

Important truth:

The default bridge network does NOT provide automatic DNS name resolution.

---

## PART 3 — User-Defined Bridge Networks (The Key Concept)

### 5. Creating Your Own Network

User-defined bridge networks DO include DNS.

#### 🧪 Exercise 4 — Create a Network

```sh
docker network create lab-net
```

Inspect it:
```sh
docker network inspect lab-net
```

**✅ Observe**

- Driver: bridge
- Containers: empty

### 6. Containers That Can Find Each Other

#### 🧪 Exercise 5 — Attach Containers to the Network

```sh
docker run -it --name a1 --network lab-net alpine sh
```

In another terminal:
```sh
docker run -it --name a2 --network lab-net alpine sh
```

Inside a2:
```sh
ping a1
```

**✅ Success**

**🧠 Why This Works**

- Both containers are on the same network
- Docker provides an internal DNS server
- Container names become hostnames

### 7. Prove DNS Is Real (Not Magic)

Inside a container:
```sh
cat /etc/resolv.conf
```

**✅ Observe**

Docker injected its own DNS resolver

Optional (advanced):
```sh
apk add --no-cache bind-tools
nslookup a1
```

---

## PART 4 — Real Application Communication

### 8. Run a Server Container

#### 🧪 Exercise 6 — Start a Web Server

```sh
docker run -d \
  --name web \
  --network lab-net \
  nginx
```

Verify:
```sh
docker ps
```

### 9. Call the Server From Another Container

```sh
docker run -it \
  --network lab-net \
  alpine sh
```

Inside:
```sh
apk add --no-cache curl
curl http://web
```

**✅ You should see HTML output**

**🧠 Key Insight**

- web is NOT localhost
- It’s a DNS name inside the Docker network

---

## PART 5 — Port Mapping Is NOT Networking

### 10. The Common Mistake

Run:
```sh
docker run -d -p 8080:80 --name web2 nginx
```

From another container:
```sh
curl http://web2
```

**❌ Fails**

**🧠 Why?**

- Port mapping exposes the container to the host
- It does NOTHING for container-to-container communication

Rule:

Port mapping is for host ↔ container, not container ↔ container

---

## PART 6 — Debugging Like an Engineer

### 11. Debugging Checklist

When something doesn’t work:

- List containers
  ```sh
  docker ps
  ```

- Inspect the network
  ```sh
  docker network inspect lab-net
  ```

- Inspect a container
  ```sh
  docker inspect <container_name>
  ```

- Enter the container
  ```sh
  docker exec -it <container_name> sh
  ```

- Test connectivity
  ```sh
  ping other_container
  curl http://other_container
  ```

Rule:

If you can’t explain it with inspect, you don’t understand it yet.

---

## PART 7 — Advanced Control

### 12. Connect a Running Container to a Network

```sh
docker network connect lab-net <container_name>
```

Re-test connectivity.

**🧠 Insight**

Docker networks are dynamic switches, not static configs.

---

## PART 8 — Dockerfile vs Networking (Critical Concept)

### 13. What Dockerfile Does NOT Do

Dockerfile:

- Builds images
- Installs software
- Defines how a container starts

Dockerfile does NOT:

- Create networks
- Attach networks
- Publish ports

Images don’t communicate. Containers do.

---

## FINAL CHALLENGE — No Instructions

### 🎯 Your Task

Using only the CLI:

- Create a Docker network
- Run:
  - One server container
  - One client container
- Make them communicate
- Prove it using:
  - ping
  - curl
  - docker network inspect

You are done when:

- You can explain why it works
- You can debug it if it breaks

### What You Know Now

- How Docker isolates networks
- What the bridge network really is
- Why DNS matters
- Why IPs are dangerous
- How containers communicate
- How to debug networking from the CLI