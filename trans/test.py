s = """The National Institute of Standards and Technology (NIST) is developing a cybersecurity
performance testbed for industrial control systems.
1 The goal of the testbed is to measure the
performance of industrial control systems (ICS) when instrumented with cybersecurity protections in
accordance with the best practices and requirements prescribed by national and international standards
and guidelines. Examples of such standards and guidelines include ISA/IEC-62443 and NIST Special
Publication 800-82 [1].
The purpose of the testbed is to emulate real-world industrial systems as closely as possible
without replicating an entire plant or assembly system. The testbed simulates a variety of industrial
scenarios that include processes with slow dynamics and others with fast dynamics. Classification of faster
versus slow is a relative determination and depends on the type of measurements being made. A slow
process is one in which changes to state occur gradually over time. Processes with fast dynamics will
exhibit a noticeable change of state soon after the system is perturbed.
Various industrial protocols are employed throughout the testbed including IP-routable and nonIP-routable protocols. Routable protocols include Internet Protocol (IP)-based protocols (e.g.,
Transmission Control Protocol (TCP) and User Datagram Protocol (UDP)) as well as industrial application
layer protocols (e.g., EtherNet/IP, Open Platform Communication (OPC), and Modbus/TCP).
Non-IP-routable protocols include legacy fieldbus protocols, such as DeviceNet. The use of nonroutable protocols allows a deeper investigation of cybersecurity with fieldbus protocols and the
controllers that make use of them; however, it was determined during the NIST Road mapping Workshop
on Industrial Control Systems Cybersecurity that non-routable protocols were of lower priority than
routable protocols. Non-routable protocols were designed to be open conduits for data flow; they were
not designed for secure communications. It is unlikely that these types of legacy protocols will be
modified to include security protections such as authentication and encryption. This design “limitation”
makes these protocols good candidates for perimeter-based security mechanisms.
Each industrial scenario is a separate enclave within the testbed, as shown in Figure 16. The first
of these scenarios is the Tennessee Eastman (TE) problem presented by Downs and Vogel [2], which is a
well-known control systems problem in chemical process manufacturing. The TE problem is an ideal
candidate for cybersecurity investigation because it is an open-loop unstable process and requires closedloop control to maintain process stability and optimize operating costs. The TE process can be considered
a process with slow dynamics in relation to the information update rate of the control network. These
slow dynamics enable an adversarial agent to compromise the control infrastructure and remain
undetected for a significant duration. Attacks that actively evade detection (stealth attacks) or attacks
that exploit specific dynamic properties of the system (geometric attacks) [3] are particularly effective
against the TE process."""

tmp = s.split("\n")
result = []
idx = 0

for i in range(len(tmp)):
    tmp[i] = tmp[i].replace("\n", "")
    if tmp[i][-1] == "." or tmp[i][-1] == "!" or tmp[i][-1] == "?":
        res = ""
        while(idx <= i):
            res = res + " " + tmp[idx]
            idx += 1
        result.append(res)
        print(idx)
        
print(result)    

