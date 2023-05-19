import { Link, useMatch, useResolvedPath} from 'react-router-dom'

const Navbar = () => {
    return ( 
        <nav className='navbar'>
            <Link to='/group' className='group'>Group21</Link>
            <ul>
                <CustomLink to='/'>Home</CustomLink>
                <CustomLink to='/map1'>OverallMap</CustomLink>
                <CustomLink to='/map'>EmploymentMap</CustomLink>
                <CustomLink to='/visualone'>LineGraph</CustomLink>
                <CustomLink to='/visualtwo'>WordCloud</CustomLink>
            </ul>
        </nav>
     );
}

function CustomLink({ to, children, ...props }) {
  const resolvedPath = useResolvedPath(to)
  const isActive = useMatch({ path: resolvedPath.pathname, end: true })
  return(
    <li className={isActive ? "active": ''}>
        <Link to={to}{...props}>{children}</Link>
    </li>
  )
}
 
export default Navbar;