import {
    Nav,
    NavLink,
    Bars,
    NavMenu,
} from '../navbarElements'
import logo from '../../../assets/logo_white.png';

const Settings = () => {
    return (
        <Nav>
            <Bars />
            <NavMenu>
                <NavLink to='/dashboard' activeStyle>
                    <img src={logo} className="dashboard-logo" alt="logo" />
                </NavLink>
                <NavLink to='/projects' activeStyle>
                    Projects
                </NavLink>
                <NavLink to='/settings' activeStyle>
                    Settings
                </NavLink>
            </NavMenu>
        </Nav>
    )
}

export default Settings