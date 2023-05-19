import GitHubIcon from '@mui/icons-material/GitHub';
import EmailIcon from '@mui/icons-material/Email';
import TwitterIcon from '@mui/icons-material/Twitter';
import './Footer.css'
import { Link } from "react-router-dom";

const Footer = () => {
    return ( 
        <div className='footer'>
          <div className='socialmedia'>
            <p>Contact us</p>
            <Link to='https://github.com/TingzhengRen/ccc_assignment2.git'>
                <button><GitHubIcon /></button>
            </Link>
            <Link to='/group'>
                <button><EmailIcon /></button>
            </Link>
            <Link to='https://twitter.com/XinyiRui'>
                <button><TwitterIcon /></button>
            </Link>
          </div>
        </div>
     );
}
 
export default Footer;