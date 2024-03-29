# Sequre Messenger

### Welcome to Sequre, the open-source messaging platform that leverages the power of quantum algorithms to provide unmatched security and privacy for all your conversations!

<img width="450" alt="Снимок экрана 2023-02-28 в 4 02 43 PM" src="https://user-images.githubusercontent.com/122756262/221979061-a8a46c61-edac-4373-98f1-b8c30631a03f.png">

## Quantum Part

Sequre employs Bell's $\ket{\Phi^+}$ state to generate two random keys for identity verification every time two users want to chat.

Our algorithm features an error-detection mechanism, using the ancilla qubit's state to identify cases where users' qubits were in the same state, ensuring the generation of keys that are impervious to any potential errors.

The quantum circuit below demonstrates the algorithm behind the key-generation process:

<img width="650" alt="image" src="https://github.com/dmitriikhitrin/sequre/assets/122756262/c2bf1b4c-1d36-491f-8895-665de4ec7e54">

The Hadamard gate is utilized to start the conversation (it says: “User0 wants to chat!”) CNOT gate identifies that user1 is connected to user0 and the pair of keys should be generated for two persons (it says: “User1 has connected to User0!”) Rotation-X gates with random angles between 0 and π/2 simulate real-system errors, while ancilla qubit is used to determine whether users’ qubits are in the same states. The dynamic circuit element checks whether the ancilla is in |1> state. If it is, the users' qubits are not in |Φ+> due to errors. Applying Pauli X-Gate on user0's qubit fixes the problem so that the users' qubits are maximally entangled again. The results of the final measurements are used to generate a pair of identical keys that ensure the privacy of the conversation.

The following histogram illustrates the probability distribution of states after 1000 runs:

<img width="467" alt="image" src="https://github.com/dmitriikhitrin/sequre/assets/122756262/74b84cf8-acb0-4901-9a96-7f3c363c3a45">

States |000> and |011> correspond to errorless experiments (in which ancilla qubit is in |0> state). The counts for |100> and |111> indicate that users' qubits were unentangled due to RX errors but were fixed by the conditional application of X-Gate.

## Backend and Frontend

We have developed backend using `FastAPI` and frontend using `Svelte` and `TailwindCSS`. Real-time messaging part is implemented using websockets. When 2 users establish a websocket connection with the server, server generates a chat room with its unique token id after which both parties can exchange messages using the established connection. 

## Demo

https://user-images.githubusercontent.com/122756262/221984729-a889c44e-9d87-46c3-931b-f495864d5a35.MP4


## Potential Upgrades

To further enhance the security of the messenger, we plan to not only compare the keys generated by the quantum provider but also require users to enter them. In the ideal scenario, both of the users would have qubits next to themselves. Users would first enter passwords to both of their qubits and then send a request with their passwords to establish a three-way websocket connection with the server. Then, the server would compare the passwords using a quantum provider and if they match, create a unique room with its token. Furthermore, the encrypting key would be generated from the passwords. Then, every message would be encrypted with the user's password and decrypted by the user's side so that server cannot access the content of the message.
