# Authenticated Gitlab DoS - Uncontrolled Resource Consumption - 8CPU cores (16vCPU) &amp; 11GB RAM - Events Tracking - Low Bandwidth

Gitlab doesn't accept 99.9% of DoS vulnerabilities. This vulnerability is out-of-scope unfortunately 😔.

`DoS vulnerabilities caused by unlimited input fields`

Out-of-scope bugs are useless noise (🗑️) — they waste time chasing irrelevant issues that don’t impact the actual target, like reporting a typo in a login page’s footer. They distract from real threats, clog reports with garbage, and show you didn’t bother reading the rules.

Submitting them is like demanding a refund for a sandwich you didn’t order.

## Video POC

[![PoC Video](https://img.youtube.com/vi/9RZuXTwYFDc/maxresdefault.jpg)](https://youtu.be/9RZuXTwYFDc)

## Quick Start

1. Clone the repository:
```
git clone https://github.com/justas-b1/Gitlab-dos3.git
cd Gitlab-dos3
```

2. Run
```
python poc.py --url "https://gitlab.example.com" --token "glpat-ME1P75un4Au_zEgiyebv"
```

## 📊 GitLab Event Flooder - Usage Guide
A Python script that sends randomized usage events to GitLab's track_event API to simulate heavy input loads with large property sets. Useful for stress testing analytics endpoints or exploring edge case behavior under unusual payload sizes.

## ✅ Required Flags

| Flag      | Description                       | Example                      |
| --------- | --------------------------------- | ---------------------------- |
| `--url`   | GitLab base URL                   | `https://gitlab.example.com` |
| `--token` | Personal access token (API token) | `glpat-xyz123`               |

## ⚙️ Optional Flags

| Flag           | Description                                   | Default |
| -------------- | --------------------------------------------- | ------- |
| `--properties` | Number of random key-value pairs to generate  | `6660`  |
| `--delay`      | Delay (in seconds) between thread starts      | `1.0`   |
| `--threads`    | Total threads (requests) to launch            | `999`   |
| `--batch`      | Number of threads before applying batch sleep | `13`    |
| `--sleep`      | Seconds to sleep after each batch             | `3`     |

## 📜 Payload Example (Truncated)

```
{
  "event": "click_blame_control_on_blob_page",
  "additional_properties": {
    "a1b2c3d4e": "xyz",
    "f5g6h7i8j": "uvw",
    "...": "..."
  }
}
```

## 🧠 Internals Overview

| Function                                    | Purpose                                                    |
| ------------------------------------------- | ---------------------------------------------------------- |
| `generate_random_string`                    | Generates random alphanumeric strings                      |
| `generate_event_with_additional_properties` | Creates a payload with randomized properties               |
| `send_request`                              | Sends the payload via `curl` and handles response          |
| `worker_thread`                             | Wraps each thread’s execution including temp file handling |
| `parse_args`                                | Parses and validates CLI arguments                         |
| `main`                                      | Main control loop for creating threads and managing timing |

## Impact

Auto-scaling under attack can cause a cost spike, potentially breaching budget thresholds or credit limits.

![Cloud Provider Response](images/cloud_provider_response.png)

**Attack Vector (AV:N)** - Attacker can exploit this remotely.

**Attack Complexity (AC:L)** - Attack uses a very simple python script.

**Privileges Required (PR:L)** - The endpoint is authenticated. Requires a simple account.

**User Interaction (UI:N)** - There's no user interaction required.

**Scope (S:C)** - Changed. Affects cloud hosting account if auto-scaling is enabled.

**Integrity Impact (I:N)** - None.

**Availability Impact (A:H)** - High. Instance becomes unavailable for at least 10 seconds and might self-restart.

From https://gitlab-com.gitlab.io/gl-security/product-security/appsec/cvss-calculator/

`When evaluating Availability impacts for DoS that require sustained traffic, use the 1k Reference Architecture. The number of requests must be fewer than the "test request per seconds rates" and cause 10+ seconds of user-perceivable unavailability to rate the impact as A:H.`

This attack used < 1RPS.

## 💡 Company Information

GitLab is a web-based DevOps platform that provides an integrated CI/CD pipeline, enabling developers to plan, develop, test, and deploy code seamlessly. Key features include:

- Version Control (Git)
- Issue Tracking 🐛
- Code Review 🔍
- CI/CD Automation 🚀

## 🏢 Who Uses GitLab?

GitLab is trusted by companies of all sizes, from startups to enterprises, including:

| Company                                            | Industry                  | Description                                                                                                                   |
| -------------------------------------------------- | ------------------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| [Goldman Sachs](https://www.goldmansachs.com/)     | Finance 💵                | A global investment bank using GitLab to modernize software pipelines and improve developer efficiency.                       |
| [Siemens](https://www.siemens.com/)                | Engineering ⚙️            | A global tech powerhouse leveraging GitLab for collaborative development in industrial automation and digital infrastructure. |
| [NVIDIA](https://www.nvidia.com/)                  | Technology 💻             | A leader in GPUs and AI computing, NVIDIA uses GitLab for scalable CI/CD and code management.                                 |
| [T-Mobile](https://www.t-mobile.com/)              | Telecommunications 📱     | Uses GitLab to manage internal tools and rapidly deliver new digital services to customers.                                   |
| [NASA](https://www.nasa.gov/)                      | Aerospace 🚀              | NASA utilizes GitLab for managing mission-critical code in scientific and engineering applications.                           |
| [Sony](https://www.sony.com/)                      | Entertainment 🎮          | Uses GitLab to support development workflows across gaming, electronics, and entertainment platforms.                         |
| [UBS](https://www.ubs.com/)                        | Banking 🏦                | A Swiss banking giant leveraging GitLab for secure, compliant DevOps in financial applications.                               |
| [Lockheed Martin](https://www.lockheedmartin.com/) | Defense & Aerospace 🛡️   | Employs GitLab for secure software development in defense systems and space technologies.                                     |
| [Shopify](https://www.shopify.com/)                | E-commerce 🛒             | Uses GitLab to scale DevOps practices and support its cloud-based e-commerce platform.                                        |
| [ING](https://www.ing.com/)                        | Financial Services 💳     | A Dutch bank adopting GitLab to improve developer collaboration and accelerate delivery.                                      |
| [CERN](https://home.cern/)                         | Scientific Research 🔬    | The European Organization for Nuclear Research uses GitLab to coordinate complex software across global teams.                |
| [Splunk](https://www.splunk.com/)                  | Data Analytics 📊         | Relies on GitLab for managing code and automating builds in its data platform ecosystem.                                      |
| [Comcast](https://corporate.comcast.com/)          | Media & Communications 📺 | Uses GitLab to streamline application delivery across their massive entertainment and broadband network.                      |
| [Deutsche Telekom](https://www.telekom.com/)       | Telecommunications 🌍     | Applies GitLab for agile development and managing cloud-native telecom infrastructure.                                        |
| [Alibaba](https://www.alibaba.com/)                | Tech & E-commerce 🧧      | One of the world’s largest tech firms, using GitLab to scale development across massive infrastructure.                       |

## 🛡️ GitLab in Defense

GitLab is favored by U.S. Department of Defense (DoD) agencies for secure, self-hosted DevSecOps environments, offering:

- On-Premise Deployment 🖥️
- Security & Compliance 🔒

Its ability to manage sensitive data and maintain operational control makes GitLab a key tool for government and defense sectors.

## Affected Websites

Shodan query: http.title:"GitLab"

Returns more than 50 thousand results.

![Shodan](images/shodan_gitlab_self_hosted.PNG)

## ⚠️ Legal Disclaimer  
This Proof-of-Concept (PoC) is provided **for educational purposes only**.  

- **Authorized Use Only**: Test only on systems you own or have explicit permission to assess.  
- **No Liability**: The author is not responsible for misuse or damages caused by this tool.  
- **Ethical Responsibility**: Do not use this tool to violate laws or exploit systems without consent.  

By using this software, you agree to these terms. 
