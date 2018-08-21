pragma solidity ^0.4.0;

contract example2{
    
    address master = 0xca35b7d915458ef540ade6068dfe2f44e8fa733c;
    uint contract_balance = 0; 

    function donate_to_master() public payable {
       contract_balance += msg.value;  
    }    
    
    function master_get_donation() public payable {
        if (contract_balance >= 100000000000000000000){
            master.transfer(contract_balance);
        } 
    }    
}

