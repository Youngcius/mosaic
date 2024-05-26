import cirq
import cirq.protocols
import cirq.protocols.kraus_protocol

depolarizing_channel = cirq.depolarize(0.01)

kraus_ops = cirq.protocols.kraus_protocol.kraus(depolarizing_channel)

print(kraus_ops)
