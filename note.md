

#### `represent_operations_in_circuit_with_local_depolarizing_noise`

As described in [Temme_2017_PRL], this function maps an `ideal_operation` $\mathcal{U}$ into its quasi-probability representation, which is a linear combination of noisy implementable operations $\sum_{\alpha} \eta_{\alpha} \mathcal{O}_{\alpha}$.

This function assumes a (local) single-qubit depolarizing noise model even for multi-qubit operations. More precisely, it assumes that the following noisy operations are implementable $\mathcal{O}_{\alpha} = \mathcal{D}^{\otimes k} \circ \mathcal{P}_{\alpha} \circ \mathcal{U}$, where $\mathcal{U}$ is the unitary associated to the input `ideal_operation` acting on $k$ qubits, $\mathcal{P}_{\alpha}$ is a Pauli operation and $\mathcal{D}(\rho) = (1 - \epsilon) \rho + \epsilon I/2$ is a single-qubit depolarizing channel ($\epsilon$ is a simple function of `noise_level`).

More information about the quasi-probability representation for a depolarizing noise channel can be found in: `represent_operation_with_global_depolarizing_noise`.

**Args:**
- ideal_operation: The ideal operation (as a QPROGRAM) to represent.
- noise_level: The noise level of each depolarizing channel.
- is_qubit_dependent: If True, the representation corresponds to the operation on the specific qubits defined in `ideal_operation`. If False, the representation is valid for the same gate even if acting on different qubits from those specified in `ideal_operation`.

**Returns:**
The quasi-probability representation of the `ideal_operation`.

**Note:**
The input `ideal_operation` is typically a QPROGRAM with a single gate but could also correspond to a sequence of more gates. This is possible as long as the unitary associated to the input QPROGRAM, followed by a single final depolarizing channel, is physically implementable.



#### `represent_operation_with_global_depolarizing_noise`

As described in [Temme_2017_PRL], this function maps an `ideal_operation` $\mathcal{U}$ into its quasi-probability representation, which is a linear combination of noisy implementable operations $\sum_{\alpha} \eta_{\alpha} \mathcal{O}_{\alpha}$.

This function assumes a depolarizing noise model and, more precisely, that the following noisy operations are implementable $\mathcal{O}_{\alpha} = \mathcal{D} \circ \mathcal{P}_{\alpha} \circ \mathcal{U}$, where $\mathcal{U}$ is the unitary associated to the input `ideal_operation` acting on $k$ qubits, $\mathcal{P}_{\alpha}$ is a Pauli operation and $\mathcal{D}(\rho) = (1 - \epsilon) \rho + \epsilon I/2^k$ is a depolarizing channel ($\epsilon$ is a simple function of `noise_level`).

For a single-qubit `ideal_operation`, the representation is as follows:

$$
\begin{align*}
\mathcal{U}_{\beta} &= \eta_1 \mathcal{O}_1 + \eta_2 \mathcal{O}_2 + \eta_3 \mathcal{O}_3 + \eta_4 \mathcal{O}_4 \\
\eta_1 &= 1 + \frac{3}{4} \frac{\epsilon}{1- \epsilon}, \quad \mathcal{O}_1 = \mathcal{D} \circ \mathcal{I} \circ \mathcal{U} \\
\eta_2 &= - \frac{1}{4}\frac{\epsilon}{1- \epsilon}, \quad \mathcal{O}_2 = \mathcal{D} \circ \mathcal{X} \circ \mathcal{U} \\
\eta_3 &= - \frac{1}{4}\frac{\epsilon}{1- \epsilon}, \quad \mathcal{O}_3 = \mathcal{D} \circ \mathcal{Y} \circ \mathcal{U} \\
\eta_4 &= - \frac{1}{4}\frac{\epsilon}{1- \epsilon}, \quad \mathcal{O}_4 = \mathcal{D} \circ \mathcal{Z} \circ \mathcal{U}
\end{align*}
$$
It was proven in [Takagi_2020_PRR] that, under suitable assumptions, this representation is optimal (minimum 1-norm).

**Args:**

- ideal_operation: The ideal operation (as a QPROGRAM) to represent.
- noise_level: The noise level (as a float) of the depolarizing channel.
- is_qubit_dependent: If True, the representation corresponds to the operation on the specific qubits defined in `ideal_operation`. If False, the representation is valid for the same gate even if acting on different qubits from those specified in `ideal_operation`.

**Returns:**
The quasi-probability representation of the `ideal_operation`.

**Note:**
This representation is based on the ideal assumption that one can append Pauli gates to a noisy operation without introducing additional noise. For a backend which violates this assumption, it remains a good approximation for small values of `noise_level`.

**Note:**
The input `ideal_operation` is typically a QPROGRAM with a single gate but could also correspond to a sequence of more gates. This is possible as long as the unitary associated to the input QPROGRAM, followed by a single final depolarizing channel, is physically implementable.





#### `cirq.kraus_to_choi`

Returns the unique Choi matrix corresponding to a Kraus representation of a channel.

Quantum channel E: L(H1) -> L(H2) may be described by a collection of operators A_i, called
Kraus operators, such that
$$
E(\rho) = \sum_i A_i \rho A_i^\dagger.
$$

Kraus representation is not unique. Alternatively, E may be specified by its Choi matrix J(E)
defined as

$$
J(E) = (E \otimes I)(|\phi\rangle\langle\phi|)
$$

where $|\phi\rangle = \sum_i|i\rangle|i\rangle$ is the unnormalized maximally entangled state
and I: L(H1) -> L(H1) is the identity map. Choi matrix is unique for a given channel.

The computation of the Choi matrix from a Kraus representation is essentially a reconstruction
of a matrix from its eigendecomposition. It has the cost of O(kd**4) where k is the number of
Kraus operators and d is the dimension of the input and output Hilbert space.

**Args:**
  - `kraus_operators`: Sequence of Kraus operators specifying a quantum channel.

**Returns:**
  - Choi matrix of the channel specified by `kraus_operators`.



```python
d = np.prod(kraus_operators[0].shape, dtype=np.int64)
choi_rank = len(kraus_operators)
k = np.reshape(np.asarray(kraus_operators), (choi_rank, d))
return np.einsum('bi,bj->ij', k, k.conj())
```

































### Modification on libraries

- Add `__hash__` method to `cirq.Circuit` class, and remove its `__hash__ = None` field
