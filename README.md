# Sequre

Welcome to Sequre, the open-source messaging platform that leverages the power of quantum algorithms to provide unmatched security and privacy for all your conversations. 

Sequre employs Bell's |Φ+⟩  state to generate two random keys for identity verification every time two users want to chat.

Our algorithm features an error-detection mechanism, using the ancilla qubit's state to identify cases where users' qubits were in the same state, ensuring the generation of keys that are impervious to any potential errors.

The quantum circuit below demonstrate the algorithm behind the key-generation process:

<img width="353" alt="image" src="https://user-images.githubusercontent.com/122756262/221970385-90f481bd-4d91-438a-a05b-8d67de1b9365.png">

Hadamard gate is utilized to start the conversation (it says: “User0 wants to chat!”) 
CNOT gates identifies that user1 is connected to user0 and the pair of keys should be generated for two persons (it says: “User1 has connected to User0!”) 
Rotation-X gates with random angles between 0 and π/2 simulate real-system errors, while ancilla qubit is used to determine whether users’ qubits are in the same states. 
After the series of measurements, the results in which ancilla qubit is in |├ 0⟩ basis state are selected to generate the pair of keys. 
If two users’ qubits are indeed entangled and QEC works, the keys happen to be identical.

The following histogram illustrates the probability distribution of states after 1024 experiments:

<img width="305" alt="image" src="https://user-images.githubusercontent.com/122756262/221971254-645712d5-3c70-4630-8125-72a506e2feb4.png">

Only states |011> and |000> participate in key-generation. Because the errors are significant, 
the probabilities of measuring system in |101> and |110> is higher than in “useful” states
