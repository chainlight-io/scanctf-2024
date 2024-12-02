// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.13;

import {Test, console} from "forge-std/Test.sol";
import {Counter} from "../src/Counter.sol";

contract CounterTest is Test {
    Counter public counter;

    function setUp() public {
        counter = new Counter();
        emit log_named_bytes("code", address(counter).code);
    }

    function test_Increment() public {
        // address(counter).call(hex"5343414e7b303436636531303238343931313138656134376265656234613363666161306166326232336463653961343235663139356366306661393131646233643463377d");
        vm.warp(1238123124);
        vm.startPrank(address(0x0), address(0x34));
        address(counter).call(
            hex"5343414e7b316165303032633662396234306265613635663265363864346363626162623566383565383562393833343438313135646535353933643730323265383235397d"
        );
        vm.stopPrank();
    }
}
