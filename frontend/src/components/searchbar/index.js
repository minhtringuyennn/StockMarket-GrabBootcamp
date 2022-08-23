// THIS FILE DESIGN THE SEARCH BAR FOR THE HEADER
import { Input, InputGroup, InputLeftElement } from "@chakra-ui/react";
import { FiSearch } from "react-icons/fi";


export default function SearchBar() {
    return (
        // Scale the width to 30% so it won't cover the size of whole header
        <InputGroup width="30%" borderColor="gray.300">
            <InputLeftElement
                pointerEvents='none'

                // This is the search icon
                children={<FiSearch />} 
            />
            <Input type='tel' placeholder='Tìm kiếm công ty' backgroundColor="white"/>
        </InputGroup>
    )
}