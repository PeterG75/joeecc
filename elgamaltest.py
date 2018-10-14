#!/usr/bin/python3
#
#	joeecc - A small Elliptic Curve Cryptography Demonstration.
#	Copyright (C) 2011-2015 Johannes Bauer
#
#	This file is part of joeecc.
#
#	joeecc is free software; you can redistribute it and/or modify
#	it under the terms of the GNU General Public License as published by
#	the Free Software Foundation; this program is ONLY licensed under
#	version 3 of the License, later versions are explicitly excluded.
#
#	joeecc is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	GNU General Public License for more details.
#
#	You should have received a copy of the GNU General Public License
#	along with joeecc; if not, write to the Free Software
#	Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
#	Johannes Bauer <JohannesBauer@gmx.de>
#

import sys

from ecc import AffineCurvePoint, ShortWeierstrassCurve, getcurvebyname
from ecc import ECPrivateKey

curve = getcurvebyname("secp521r1")

def msg_to_point(curve, msg, msg_width_bits):
	int_message = int.from_bytes(msg, byteorder = "little")
	for i in range(100):
		try_message = int_message | (i << msg_width_bits)
		point = curve.getpointwithx(try_message)
		if point:
			point = point[0]
			break
	return point

def elgamal_encrypt(recipient_pubkey, msg, msg_width_bits):
	k = ECPrivateKey.generate(curve)
	C1 = k.pubkey.point
	C2 = k.scalar * recipient_pubkey.point
	P_m = msg_to_point(curve, msg, msg_width_bits = msg_width_bits)
	ciphertext = (C1, C2 + P_m)
	return ciphertext

def elgamal_decrypt(recipient_privkey, ciphertext, msg_width_bits):
	(C1, C2) = ciphertext
	Cp = C1 * recipient_privkey.scalar
	P_m = C2 + (-Cp)
	int_message = int(P_m.x) & ((1 << msg_width_bits) - 1)
	msg = int.to_bytes(int_message, byteorder = "little", length = (msg_width_bits + 7) // 8)
	return msg


privkey = ECPrivateKey.generate(curve)
pubkey = privkey.pubkey

message = b"foobar"
print("Message:", message)
ciphertext = elgamal_encrypt(pubkey, message, msg_width_bits = 256)
print("Ciphertext:")
print("    C1 =", ciphertext[0])
print("    C2 =", ciphertext[1])
plaintext = elgamal_decrypt(privkey, ciphertext, msg_width_bits = 256)
print("Plaintext:", plaintext)