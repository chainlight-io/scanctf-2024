// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.13;

import {Test, console} from "forge-std/Test.sol";

contract Counter is Test {
    function rsaEncrypt(bytes memory _data, uint256 _publicKey) internal returns (uint256[] memory) {
        uint256[] memory encryptedData = new uint256[](_data.length / 2 + 1);
        uint256 e = 65537;
        uint256 n = _publicKey;

        uint256 z = 0;

        for (uint256 i = 0; i < _data.length; i += 2) {
            uint256 max = uint256(uint256(keccak256(abi.encodePacked(block.timestamp))) + z) % 1_000_000;
            for (uint256 j = 0; j < max; j++) {
                z += 1;
            }

            uint256 m = 0;
            if (i < _data.length) {
                m = uint256(uint8(_data[i]));
            }
            if (i + 1 < _data.length) {
                m += uint256(uint256(uint8(_data[i + 1])) << 8);
            }

            m += uint256((uint16(uint8(bytes32(uint256(uint160(tx.origin)))[31])) + z) & 0xff) << 16;

            uint256 c = modexp(m, e, n);
            encryptedData[i / 2] = c;
        }
        return encryptedData;
    }

    function modexp(uint256 base, uint256 exp, uint256 mod) internal pure returns (uint256) {
        require(mod > 0);
        if (mod == 1) return 0;
        if (exp == 0) return 1;

        uint256 result = 1;
        uint256 baseMod = base % mod;

        while (exp > 0) {
            if (exp % 2 == 1) {
                result = safeMulMod(result, baseMod, mod);
            }
            baseMod = safeMulMod(baseMod, baseMod, mod);
            exp /= 2;
        }

        return result;
    }

    function safeMulMod(uint256 a, uint256 b, uint256 mod) internal pure returns (uint256) {
        require(mod > 0);

        uint256 result = 0;
        uint256 tempB = b % mod;

        while (a > 0) {
            if (a % 2 == 1) {
                result = (result + tempB) % mod;
            }
            tempB = (tempB * 2) % mod;
            a /= 2;
        }
        return result;
    }

    fallback() external {
        /*
        >>> 1049689677999788387637650154823 * 846446199109894139772259043893
            888505838187809547711833896999795292417866051889833402645939

            >> 949682225412977198398142321867*839704106970368912668345211987
        797452064996036607633741733398429157877438385639196500619729
        */
        // emit log_named_uint("a", userInput.length);
        uint256[] memory output = rsaEncrypt(msg.data, 797452064996036607633741733398429157877438385639196500619729); // 3*7

        bytes memory realOutput = abi.encodePacked(output);
        uint256 length = realOutput.length;
        assembly {
            return(add(realOutput, 0x20), length)
        }
    }
}
