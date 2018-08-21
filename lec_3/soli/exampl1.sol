pragma solidity ^0.4.0;

contract example1{
           
    function send_to_address(address to) public payable {
       to.transfer(msg.value);
    }    

}