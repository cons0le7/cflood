
**This is a modified version forked from the original which no longer contains the vulnerable go server, instead the script allows you to input a target host. This is strictly for educational purposes with the intent of offering more flexibility to test this POC in a home lab or professional setting. USING THIS AGAINST ANY TARGET WITHOUT PERMISSION IS HIGHLY UNETHICAL AND ILLEGAL. I am not reponsible for any use or misuse of this tool.**

-Now includes a tool to check if servers are HTTP/2 capable.-


# PoC: HTTP/2 CONTINUATION Flood Vulnerability
This is a proof of concept for the HTTP/2 CONTINUATION flood vulnerability published by 
[nowotarski.info](https://nowotarski.info/) on April 03, 2024.  

This vulnerability can lead to different consequences for vulnerable web servers:
- CPU exhaustion
- Out Of Memory crash (After a single or multiple connections)
- Crash after a few frames sent  

(more details in [the blog post of nowotarski](
https://nowotarski.info/http2-continuation-flood-technical-details/))


Install the required prerequisites:
```shell
pip install h2
```

Execute the Proof of Concept:
```shell
cd cflood
python3 start.py
```

![IMG_9380](https://github.com/user-attachments/assets/db8854b6-9a19-4556-8a5f-b651758ff2b4)
![IMG_9379](https://github.com/user-attachments/assets/24085cef-e437-4e65-b2e5-242bfb603148)


## Affected CVEs
- CVE-2024-27983
- CVE-2024-27919
- CVE-2024-2758
- CVE-2024-2653
- CVE-2023-45288
- CVE-2024-28182
- CVE-2024-27316
- CVE-2024-31309
- CVE-2024-30255

## References
- [HTTP/2 CONTINUATION Flood: Technical Details](https://nowotarski.info/http2-continuation-flood-technical-details/)
- [HTTP/2 CONTINUATION frames can be utilized for DoS attacks](https://kb.cert.org/vuls/id/421644)
