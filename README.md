<p align="center">
  <img src="assets/hero.svg" alt="MAKU — Platform Engineer" width="100%" />
</p>

<p align="center">
  <picture>
    <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=500&size=20&pause=1000&color=A66BFF&center=true&vCenter=true&width=600&lines=Connecting+people%2C+systems+and+ideas;Building+reliable+platforms;Embedded+and+reverse+engineering;Running+a+homelab+that+never+sleeps" alt="Typing SVG" />
  </picture>
</p>

<p align="center">
  <img src="https://komarev.com/ghpvc/?username=Maku-hub&color=6e40c9&style=for-the-badge&label=PROFILE+VIEWS" alt="Profile views" />
  <br />
  <a href="https://github.com/Maku-hub?tab=followers"><img src="https://img.shields.io/github/followers/Maku-hub?style=for-the-badge&logo=github&label=followers&labelColor=0d1117&color=8957e5" alt="Followers" /></a>
  <a href="https://github.com/Maku-hub?tab=repositories"><img src="https://img.shields.io/github/stars/Maku-hub?style=for-the-badge&logo=github&label=stars&labelColor=0d1117&color=bd561d" alt="Total stars" /></a>
  <a href="https://maku-hub.github.io/whoami"><img src="https://img.shields.io/website?url=https%3A%2F%2Fmaku-hub.github.io%2Fwhoami&style=for-the-badge&label=whoami&labelColor=0d1117&up_message=online&down_message=offline&up_color=238636&down_color=b62324" alt="whoami website status" /></a>
  <img src="https://img.shields.io/github/last-commit/Maku-hub/Maku-hub?style=for-the-badge&label=last+commit&labelColor=0d1117&color=1b7c83" alt="Last commit" />
  <a href="https://github.com/Maku-hub/Maku-hub/actions/workflows/profile.yml"><img src="https://img.shields.io/github/actions/workflow/status/Maku-hub/Maku-hub/profile.yml?style=for-the-badge&label=profile+build&labelColor=0d1117" alt="Profile build status" /></a>
</p>

<img src="assets/divider.svg" alt="" width="100%" />

### 💻 whoami

<p align="center">
  <img src="assets/terminal.svg" alt="Terminal session: Maku, Platform Engineer" width="100%" />
</p>

<img src="assets/divider.svg" alt="" width="100%" />

### 🌳 Public projects over time

<p align="center">
  <img src="assets/generated/gitlog.svg" alt="Git log graph of Maku's public repositories" width="100%" />
</p>

<img src="assets/divider.svg" alt="" width="100%" />

### 🕒 Recent commits

<p align="center">
  <img src="assets/generated/commits.svg" alt="The ten most recent commits across Maku's public repositories" width="100%" />
</p>

<img src="assets/divider.svg" alt="" width="100%" />

### 🧬 Code DNA

<p align="center">
  <img src="assets/generated/languages.svg" alt="Language breakdown across public repositories" width="100%" />
</p>

<img src="assets/divider.svg" alt="" width="100%" />

### ♾️ How I work

<p align="center">
  <img src="assets/loop.svg" alt="DevSecOps infinity loop: plan, code, build, test, release, deploy, operate, monitor — with security in the middle" width="100%" />
</p>

<div align="center">
<details>
<summary><i>Security isn't a stage. It's the thing every stage passes through.</i></summary>
<br>

```mermaid
flowchart LR
    commit([git push]) --> lint[Lint &amp; format]
    lint --> secrets{{Secret scan}}
    secrets --> sast{{SAST}}
    sast --> tests[Unit &amp; integration tests]
    tests --> build[Build image]
    build --> sca{{SCA &amp; image scan}}
    sca --> sbom[SBOM]
    sbom --> sign[Sign artifact]
    sign --> deploy[Deploy]
    deploy --> dast{{DAST}}
    dast --> monitor[(Monitor &amp; alert)]
    monitor -. feedback .-> commit

    classDef sec fill:#ff6a00,stroke:#ff6a00,color:#fff
    classDef step fill:#1e1b2e,stroke:#a66bff,color:#fff
    class secrets,sast,sca,dast sec
    class lint,tests,build,sbom,sign,deploy,monitor step
```

</details>
</div>

$$
\text{reliability} = \frac{\text{automation} \times \text{monitoring}}{\text{manual steps} + \varepsilon}
$$

<img src="assets/divider.svg" alt="" width="100%" />

### 🐄 Quote of the day

<p align="center">
  <img src="assets/generated/fortune.svg" alt="Quote of the day, said by an ASCII cow" width="100%" />
</p>

<img src="assets/divider.svg" alt="" width="100%" />

### 🚩 Capture the flag

<p align="center">
  <img src="assets/ctf.svg" alt="Capture the flag: three hidden flags — #01 encoding, hidden in plain sight; #02 forensics, somewhere in a dump; #03 steganography, images have source code too. Format: flag{...}" width="100%" />
</p>

<!-- flag 1/3: ZmxhZ3t5MHVfZjB1bmRfbTRrdX0= -->

<details>
<summary><code>$ xxd /dev/maku</code> — memory dump</summary>
<br>

```console
00000000: 4d41 4b55 2d48 5542 202f 2f20 504c 4154  MAKU-HUB // PLAT
00000010: 464f 524d 2045 4e47 0a73 796e 747b 7533  FORM ENG.synt{u3
00000020: 6b5f 7a34 6578 665f 6775 335f 6663 3067  k_z4exf_gu3_fc0g
00000030: 7d0a 2d2d 206e 6f74 2065 6e63 7279 7074  }.-- not encrypt
00000040: 696f 6e20 2d2d 0a                        ion --.
```

</details>

<details>
<summary><code>$ ./cheats</code> — <kbd>↑</kbd> <kbd>↑</kbd> <kbd>↓</kbd> <kbd>↓</kbd> <kbd>←</kbd> <kbd>→</kbd> <kbd>←</kbd> <kbd>→</kbd> <kbd>B</kbd> <kbd>A</kbd></summary>
<br>

> [!TIP]
> **+30 lives.** Hints unlocked:
> 1. Base64 is an encoding, not a secret.
> 2. ROT13 is a substitution, not a cipher you should trust.
> 3. Open [`assets/hero.svg`](assets/hero.svg) and switch to Code view.

</details>

<details>
<summary><code>$ cat /.well-known/security.txt</code> — responsible disclosure</summary>
<br>

```text
# Found something? Responsible disclosure welcome.
Contact: https://maku-hub.github.io/whoami
Preferred-Languages: pl, en
Policy: be kind, be specific, include a PoC
Acknowledgments: you, in this file, if you find all three flags
Expires: never — this README maintains itself
```

</details>

<br>

<img src="assets/divider.svg" alt="" width="100%" />
