---
title: Post-Quantum Cryptography Overview
description: Learn how to create a quantum safe PKI using post-quantum cryptography (PQC) with PKIaaS.io.
---
Post-quantum cryptography (PQC) refers to cryptographic algorithms designed to remain secure against the potential threats posed by quantum computers. Quantum computers have the potential to break many of the cryptographic algorithms that are currently in use, including RSA and ECC. As a result, the National Institute of Standards and Technology (NIST) has been working to standardize post-quantum cryptographic algorithms.

On August 13, 2024, NIST finalized two digital signature standards that can be used to create quantum-safe X.509 certificates: ML-DSA (formerly Dilithium), as defined in [FIPS 204](https://csrc.nist.gov/pubs/fips/204/final), and SLH-DSA, as defined in [FIPS 205](https://csrc.nist.gov/pubs/fips/205/final). PKIaaS.io currently supports ML-DSA. Support for SLH-DSA is planned for a future release.

* [ML-DSA](ml-dsa.md)