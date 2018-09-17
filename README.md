```
shortname: BEP-22
name: Proxy Re-Encryption Demo 1
type: Standard
status: Raw
editor: Troy McConaghy <troy@bigchaindb.com>
contributors: Gautam Dhameja <gautam@bigchaindb.com>
```

# Abstract

This BEP outlines the code that should be written as an initial demo of how one can use proxy re-encryption with BigchainDB.

# Motivation

Potential BigchainDB users often ask about how they can keep some data private, or private-for-some. There are many options. One useful building block is _proxy re-encryption_. It would be nice if there was some example code (with documentation) showing a way to use proxy re-encryption with BigchainDB.

Why proxy re-encryption?

Suppose Dan owns some data and wants to store it, encrypted, in a BigchainDB network, so that others can decrypt it. To encrypt it for Megan, he could encrypt it using Megan's public key and store the ciphertext in BigchainDB. Then Megan could decrypt it with her private key, and nobody else could decrypt it. To encrypt it for Todd, Dan would have to encrypt his data a second time, using Todd's public key, and he'd have to store _that_ ciphertext (for Todd) in BigchainDB too!

This is not a scalable approach in case of many messages and recipients. Another major drawback of this method is it requires Dan to be online and perform cryptographic operations everytime new access should be granted. This significantly limits the access management flexibility. 

Not only Dan would like to store only one ciphertext in BigchainDB, but he'd also like to give selective access to recipients in the future, as needed. Proxy re-encryption is one way to enable that, but it would be nice to have some code demonstrating _how_.

# Specification

The code developed for this BEP/demo must work with [Skycryptor's](http://skycryptor.com/) code for proxy re-encryption. (Note: That code is written in C++ but has Python bindings.)

All the changes to the drivers (described below) should be implemented in the Python Driver first.

"BigNet" is the name of a BigchainDB network that is set up by whoever does this demo.

## A Usage Story

To understand the required software and what it must do, we wrote this story:

- Dan is a data owner.
- Dan generates an ed25519 key-pair for signing and verifying BigchainDB-related things.
- Dan generates an secp256k1 key-pair for encrypting and decrypting messages.
- Dan prepares and signs a BigchainDB CREATE transaction to associate his two public keys:

  - `inputs[0].owners_before[0]` = Dan's ed25519 public key (verifying key)
  - `asset.data.type = "public key linker"`
  - `asset.data.secp256k1_public_key` = Dan's secp256k1 public key (encryption key)
  - `asset.data.public_id` = Dan's public identifier (email or username)

- Dan posts that transaction to BigNet.
- Dan encrypts confidential message_1 (a string) to create ciphertext_1 (a string), using his secp256k1 public key.
- Dan prepares and signs a BigchainDB CREATE transaction to store ciphertext_1:

  - `inputs[0].owners_before[0]` = Dan's ed25519 public key (verifying key)
  - `asset.data.type = "ciphertext storage"`
  - `asset.data.ciphertext` = ciphertext_1

- Dan posts that transaction to BigNet.
- Megan wants to read message_1.
- Megan generates an secp256k1 keypair
- Megan generates an ed25519 key pair. Although Megan could be identified by her secp256k1 public key only, signing key will be used to sign the "public key linker" and all subsequent transactions. (e.g. "access request" transactions) 
- Megan prepares and signs a "public key linker" transaction (as above) and posts it to BigNet.
- Megan contacts Dan with the transaction ID of Megan’s "public key linker" transaction, and requests the right to read message_1. FIXME: Maybe that request should itself be a signed transaction, signed by Megan’s ed25519 signing key? (Aram's comment: I agree that this request should be a signed "Access Request" transaction, signed by Megan's key) 
- if Dan is not okay with Megan's request, he probably can create new "Reject Access request" transaction linked to the original "Access request" FIXME: Describe this "Reject Access Request" transaction details.
- If Dan is okay with Megan reading message_1, then Dan creates a proof that Megan has the right to read message_1, a signed BigchainDB CREATE transaction with:

  - `inputs[0].owners_before[0]` = Dan's ed25519 public key (verifying key)
  - `asset.data.type = "permission to read"`
  - `asset.data.transaction_id` = The BigchainDB transaction ID of the transaction containing ciphertext_1
  - `asset.data.secp256k1_public_key` = Megan's public secp256k1 encryption key

- Dan posts that transaction to BigNet.
- Dan generates a special re-encryption key denoted as _re_encryption_key_dan_megan_ by using Skycryptor's re-encryption key generation function. This step is performed on Dan's device using Dan's secp256k1 private key and Megan's secp256k1 public key.
- Dan sends this re-encryption key to Proxy Service among with other auxiliary data FIXME: Proxy Service should provide a special API enabling  Dan to make a POST request.
  - `data.delegator_id` = Dan's public identifier 
  - `data.delegatee_id` = Megan's public identifier
  - `data.re_encryption_key` = re_encryption_key_dan_megan
  - `data.timestamp` = timestamp
  - `data.signature` = Signature under Dan's ed25519 public key.
  - `....`
  
- The Proxy Service stores this record in a private local database (only accessible to the Proxy Service). 
- Once the re-encryption key is created by Dan for Megan, the Proxy Service will be able to serve Megan's re-encryption requests. 
- Proxy Service will provide an API for re-encryption requests. Each re-encryption request will contain the following information
  - `data.ciphertext` = ciphertext_1 OR `data.ciphertext` = The BigchainDB transaction ID of the transaction containing ciphertext_1
  - `data.requesting_user_id` = Megan's public identifier
  - `data.request_signature` = Request signature under the Megan's public ed25519 key
   
- When the Proxy Service gets a "Re-Encryption Request" from Megan (signed by Megan's ed25519 signing key), it checks for a transaction in BigNet to make sure Megan has the right to read message 1 (given by Dan, signed by Dan). FIXME: This Re-Encryption request can be recorded in the BigNet too in order to leave an immutable trace.
- If the permission check is successful and Megan is allowed to read the ciphertext_1, The Proxy Service takes the ciphertext_1 from the BigNet and the _re_encryption_key_dan_megan_ from its private database and performs a _ReEncrypt_ operation, which transforms the ciphertext_1 into ciphertext_2. The resulted ciphertext_2 is already encrypted under Megan's public secp256k1 key.
- The Proxy Service sends ciphertext_2 to Megan. _FIXME: Two possible ways for returning the ciphertext_2 to Megan a. Proxy Service can return it as a parameter of the original GET request b. Proxy Service can create a "Re-Encrypted Data" Transaction on the BigNet and return the transaction ID to Megan as a GET request return parameter_.  
- Megan gets the ciphertext_2 (either by reading it from the BIGNET or from the original re-encryption request return data) and decrypts it into message_1 using her private secp256k1 decryption key.

## Required Additions or Changes to the BigchainDB Driver


FIXME: Please ignore this section until we’re all in agreement on the Usage Story above. This section falls out of the usage story.

- A method to generate an secp256k1 keypair, similar to the driver's existing method for generating an ed25519 keypair.
- A convenience method to generate a signed CREATE transaction linking an ed25519 public key to an secp256k1 public key (signed by the corresponding ed25519 private key).

  - `inputs[0].owners_before[0]` = ed25519 public key (encoded as a Base58 string as per [BEP-13](https://github.com/bigchaindb/BEPs/tree/master/13#cryptographic-keys-and-signatures))
  - `asset.data.type = "public key linker"`
  - `asset.data.secp256k1_public_key` = secp256k1 public key. FIXME: How should the secp256k1 public key be encoded in the JSON string? Base58? Base64? Hex? What does Skycryptor prefer?
  - Note 1: The ed25519 public key might also be stored in the values of `outputs[0].public_keys[0]` and `outputs[0].condition.details.public_key`, but that is not required and those values might not contain the ed25519 public key.
  - Note 2: The transaction associating the ed25519 and secp256k1 public keys might be modified so that it better conforms with some standard such as [Decentralized Identifiers (DIDs)](https://w3c-ccg.github.io/did-spec/). At a minimum, it must contain those two public keys and it must be signed by the corresponding ed25519 private (signing) key.

- A convenience method or function taking a string and an secp256k1 encryption key as input, and returning the ciphertext. FIXME: How should the ciphertext be encoded? What does Skycryptor software prefer?
- FIXME: I can finish this once the story is clear. -Troy

## Tooling Required by the Proxy Service

FIXME: I can finish this once the story is clear. -Troy

# Change Process

BigchainDB GmbH has a process to improve BEPs like this one. Please see [BEP-1 (C4)](../1) and [BEP-2 (COSS)](../2).

# Implementation

Once an implementation exists, add links here.

# Copyright Waiver

<p xmlns:dct="http://purl.org/dc/terms/">
  <a rel="license"
     href="http://creativecommons.org/publicdomain/zero/1.0/">
    <img src="http://i.creativecommons.org/p/zero/1.0/88x31.png" style="border-style: none;" alt="CC0" />
  </a>
  <br />
  To the extent possible under law, all contributors to this BEP
  have waived all copyright and related or neighboring rights to this BEP.
</p>


