
# Quagga [![Build Status](https://travis-ci.com/HPI-Information-Systems/QuaggaLib.svg?branch=master)](https://travis-ci.com/HPI-Information-Systems/QuaggaLib)
An email segmentation system:
- reference implementation of ECIR 2018 paper

# Reference

> Repke, Tim and Krestel R. *Bringing Back Structure to Free Text Email Conversations with Recurrent Neural Networks.* ECIR 2018

### Abstract
Email communication plays an integral part of everybody’s
life nowadays. Especially for business emails, extracting and analysing
these communication networks can reveal interesting patterns of processes
and decision making within a company. Fraud detection is another
application area where precise detection of communication networks is
essential. In this paper we present an approach based on recurrent neural
networks to untangle email threads originating from forward and reply
behaviour. We further classify parts of emails into 2 or 5 zones to capture
not only header and body information but also greetings and signatures.
We show that our deep learning approach outperforms state-of-the-art
systems based on traditional machine learning and hand-crafted rules.
Besides using the well-known Enron email corpus for our experiments,
we additionally created a new annotated email benchmark corpus from
Apache mailing lists.

# Setup
### Installation
```python setup.py install```



