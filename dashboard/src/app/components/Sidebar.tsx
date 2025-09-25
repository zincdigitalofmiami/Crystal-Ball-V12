'use client'

import { useState } from 'react'
import { 
  Navbar, 
  NavbarBrand, 
  NavbarContent, 
  NavbarItem, 
  Link, 
  Button,
  Dropdown,
  DropdownTrigger,
  DropdownMenu,
  DropdownItem
} from '@heroui/react'
import { 
  ChevronDownIcon,
  Squares2X2Icon,
  DocumentTextIcon,
  CodeBracketIcon
} from '@heroicons/react/24/outline'

export default function Sidebar() {
  const [isMenuOpen, setIsMenuOpen] = useState(false)

  return (
    <Navbar 
      isBordered 
      isMenuOpen={isMenuOpen}
      onMenuOpenChange={setIsMenuOpen}
      className="bg-gray-900 border-gray-700"
    >
      <NavbarContent>
        <NavbarBrand>
          <div className="flex items-center space-x-3">
            <div className="w-8 h-8 bg-white rounded-lg flex items-center justify-center">
              <Squares2X2Icon className="w-5 h-5 text-gray-900" />
            </div>
            <div>
              <p className="text-white font-bold text-lg">US Oil Solutions</p>
              <p className="text-gray-400 text-xs">Palo Alto, CA</p>
            </div>
            <ChevronDownIcon className="w-4 h-4 text-gray-400" />
          </div>
        </NavbarBrand>
      </NavbarContent>

      <NavbarContent className="hidden sm:flex gap-4" justify="center">
        <NavbarItem isActive>
          <Link 
            href="/" 
            className="text-white data-[active=true]:text-blue-400"
            aria-current="page"
          >
            <Squares2X2Icon className="w-5 h-5 mr-2" />
            Dashboard
          </Link>
        </NavbarItem>
        <NavbarItem>
          <Link 
            href="/news-sentiment" 
            className="text-gray-400 hover:text-white"
          >
            <DocumentTextIcon className="w-5 h-5 mr-2" />
            News Sentiment
          </Link>
        </NavbarItem>
        <NavbarItem>
          <Link 
            href="/strategy" 
            className="text-gray-400 hover:text-white"
          >
            <CodeBracketIcon className="w-5 h-5 mr-2" />
            Strategy
          </Link>
        </NavbarItem>
      </NavbarContent>

      <NavbarContent justify="end">
        <NavbarItem>
          <Button 
            as={Link} 
            color="primary" 
            href="#" 
            variant="flat"
            className="bg-blue-600 text-white"
          >
            Feedback?
          </Button>
        </NavbarItem>
        <NavbarItem>
          <Button 
            as={Link} 
            color="primary" 
            href="#" 
            variant="flat"
            className="bg-gray-700 text-white"
          >
            🔔 2
          </Button>
        </NavbarItem>
        <NavbarItem>
          <Button 
            as={Link} 
            color="primary" 
            href="#" 
            variant="flat"
            className="bg-gray-700 text-white"
          >
            ?
          </Button>
        </NavbarItem>
        <NavbarItem>
          <Button 
            as={Link} 
            color="primary" 
            href="#" 
            variant="flat"
            className="bg-gray-700 text-white"
          >
            GitHub
          </Button>
        </NavbarItem>
        <NavbarItem>
          <Button 
            as={Link} 
            color="primary" 
            href="#" 
            variant="flat"
            className="bg-gray-700 text-white"
          >
            👤
          </Button>
        </NavbarItem>
      </NavbarContent>
    </Navbar>
  )
}
