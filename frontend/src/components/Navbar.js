import React, { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import {
  AppBar,
  Toolbar,
  Button,
  Container,
  Box,
  IconButton,
  Menu,
  MenuItem,
  Typography,
  Avatar,
} from '@mui/material';
import {
  Home as HomeIcon,
  AutoAwesome as GenerateIcon,
  Preview as PreviewIcon,
  Image as ImageIcon,
  AccountCircle,
  Logout,
} from '@mui/icons-material';
import { useAuth } from '../context/AuthContext';

function Navbar() {
  const navigate = useNavigate();
  const location = useLocation();
  const { user, logout } = useAuth();
  const [anchorEl, setAnchorEl] = useState(null);

  const isActive = (path) => location.pathname === path;

  const handleMenu = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  const handleLogout = async () => {
    try {
      await logout();
      navigate('/login');
    } catch (error) {
      console.error('Logout failed:', error);
    }
    handleClose();
  };

  return (
    <AppBar position="static" color="default" elevation={1}>
      <Container maxWidth="lg">
        <Toolbar disableGutters>
          <Box sx={{ flexGrow: 1, display: 'flex', gap: 2 }}>
            <Button
              color="inherit"
              startIcon={<HomeIcon />}
              onClick={() => navigate('/')}
              sx={{
                backgroundColor: isActive('/') ? 'rgba(0, 0, 0, 0.04)' : 'transparent',
              }}
            >
              Home
            </Button>
            {user && (
              <>
                <Button
                  color="inherit"
                  startIcon={<GenerateIcon />}
                  onClick={() => navigate('/generate')}
                  sx={{
                    backgroundColor: isActive('/generate') ? 'rgba(0, 0, 0, 0.04)' : 'transparent',
                  }}
                >
                  Generate
                </Button>
                <Button
                  color="inherit"
                  startIcon={<PreviewIcon />}
                  onClick={() => navigate('/preview')}
                  sx={{
                    backgroundColor: isActive('/preview') ? 'rgba(0, 0, 0, 0.04)' : 'transparent',
                  }}
                >
                  Preview
                </Button>
                <Button
                  color="inherit"
                  startIcon={<ImageIcon />}
                  onClick={() => navigate('/images')}
                  sx={{
                    backgroundColor: isActive('/images') ? 'rgba(0, 0, 0, 0.04)' : 'transparent',
                  }}
                >
                  Images
                </Button>
              </>
            )}
          </Box>

          <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
            {user ? (
              <>
                <Typography variant="body2" sx={{ mr: 2 }}>
                  {user.email}
                </Typography>
                <IconButton
                  onClick={handleMenu}
                  size="small"
                  sx={{ ml: 2 }}
                  aria-controls={Boolean(anchorEl) ? 'account-menu' : undefined}
                  aria-haspopup="true"
                  aria-expanded={Boolean(anchorEl) ? 'true' : undefined}
                >
                  <Avatar sx={{ width: 32, height: 32 }}>
                    <AccountCircle />
                  </Avatar>
                </IconButton>
                <Menu
                  anchorEl={anchorEl}
                  id="account-menu"
                  open={Boolean(anchorEl)}
                  onClose={handleClose}
                  onClick={handleClose}
                  transformOrigin={{ horizontal: 'right', vertical: 'top' }}
                  anchorOrigin={{ horizontal: 'right', vertical: 'bottom' }}
                >
                  <MenuItem onClick={handleLogout}>
                    <Logout sx={{ mr: 1 }} /> Logout
                  </MenuItem>
                </Menu>
              </>
            ) : (
              <>
                <Button
                  color="inherit"
                  onClick={() => navigate('/login')}
                  sx={{
                    backgroundColor: isActive('/login') ? 'rgba(0, 0, 0, 0.04)' : 'transparent',
                  }}
                >
                  Login
                </Button>
                <Button
                  color="inherit"
                  onClick={() => navigate('/register')}
                  sx={{
                    backgroundColor: isActive('/register') ? 'rgba(0, 0, 0, 0.04)' : 'transparent',
                  }}
                >
                  Register
                </Button>
              </>
            )}
          </Box>
        </Toolbar>
      </Container>
    </AppBar>
  );
}

export default Navbar; 