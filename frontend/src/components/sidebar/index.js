// THIS FILE CONTAINS THE SIDEBAR AND HEADER USED FOR ANY PAGE OF THE WEBAPP
import {
    Box,
    CloseButton, Drawer,
    DrawerContent, Flex, Icon, IconButton, Text, useColorModeValue, useDisclosure
} from '@chakra-ui/react';
import React from 'react';
import {
    FiCompass, FiHome, FiMenu, FiSettings, FiStar, FiTrendingUp
} from 'react-icons/fi';
import { Link } from 'react-router-dom';
import SearchBar from '../searchbar';

// List of items on the sidebar, controlled by the NavItem component below
const LinkItems = [
    { name: 'Trang chủ', icon: FiHome , to: "/"},
    { name: 'Bộ lọc cổ phiếu', icon: FiTrendingUp , to: "/xxx"},
    { name: 'Định giá doanh nghiệp', icon: FiCompass , to: "/company/VIC"},
    { name: 'Xếp hạng công ty', icon: FiStar , to: "/xxx"},
    { name: 'Về chúng tôi', icon: FiSettings , to: "/xxx"},
];


// Initialize sidebar and header
export default function SidebarWithHeader({
    children,
}) {
    const { isOpen, onOpen, onClose } = useDisclosure();
    return (
        <Box minH="100vh" >
            <SidebarContent
                onClose={() => onClose}
                display={{ base: 'none', md: 'block' }}
                color={"gray.200"}
            />
            <Drawer
                autoFocus={false}
                isOpen={isOpen}
                placement="left"
                onClose={onClose}
                returnFocusOnClose={false}
                onOverlayClick={onClose}
                size="full">
                <DrawerContent>
                    <SidebarContent onClose={onClose} />
                </DrawerContent>
            </Drawer>

            {/* Now the header comes in */}
            <MobileNav onOpen={onOpen} />
            <Box ml={{ base: 0, md: 60 }} pl="8">
                {children}
            </Box>
        </Box>
    );
}

// Design the Sidebar and its contents
const SidebarContent = ({ onClose, ...rest }) => {
    return (
        <Box
            transition="3s ease"
            bg={useColorModeValue('#007F21', 'gray.900')}
            borderRight="1px"
            borderRightColor={useColorModeValue('gray.200', 'gray.700')}
            w={{ base: 'full', md: "260px" }}
            pos="fixed"
            h="full"
            {...rest}>
            <Flex h="20" alignItems="center" mx="8" justifyContent="space-between" textAlign="center">
                <Text fontSize="4xl" fontFamily="Roboto Slab" fontWeight="bold">
                    HẺ-CU-LÉ
                </Text>
                <CloseButton display={{ base: 'flex', md: 'none' }} onClick={onClose} />
            </Flex>
            {LinkItems.map((link) => (
                
                <NavItem key={link.name} to={link.to} icon={link.icon}>
                
                    {link.name}
                </NavItem>
            ))}
        </Box>
    );
};

// Design and format the items in the sidebar, add their additional icons
const NavItem = ({ to, icon, children, ...rest }) => {
    return (
        <Link to={to} style={{ textDecoration: 'none' }} _focus={{ boxShadow: 'none' }}>
            <Flex
                align="center"
                p="4"
                mx="4"
                borderRadius="lg"
                role="group"
                cursor="pointer"
                _hover={{
                    bg: '#58E37C',
                    color: 'white',
                }}
                {...rest}>
                {icon && (
                    <Icon
                        mr="4"
                        fontSize="16"
                        _groupHover={{
                            color: 'white',
                        }}
                        as={icon}
                    />
                )}
                {children}
            </Flex>
        </Link>
    );
};

// This is to design the header with a search bar in it
const MobileNav = ({ onOpen, ...rest }) => {
    return (
        <Flex
            ml={{ base: 0, md: 0 }}
            px={{ base: 0, md: 0 }}
            height="20"
            alignItems="center"
            bg={useColorModeValue('#02B04E', 'gray.900')}
            borderBottomWidth="1px"
            borderBottomColor={useColorModeValue('gray.200', 'gray.700')}
            justifyContent={{ base: 'space-between', md: 'center' }}
            {...rest}>
            <IconButton
                display={{ base: 'flex', md: 'none' }}
                onClick={onOpen}
                variant="outline"
                aria-label="open menu"
                icon={<FiMenu />}
            />
            
            {/* Insert the Searchbar in the middle of the header */}
            <SearchBar/> 

            {/* This is to scale for mobile view, currently not necessary */}
            {/* <Text
                display={{ base: 'flex', md: 'none' }}
                fontSize="2xl"
                fontFamily="monospace"
                fontWeight="bold">
                Logo
            </Text> */}
        </Flex>
    );
};