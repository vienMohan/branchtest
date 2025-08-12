import React from "react";
import { Grid, Typography, Box, IconButton, Container } from "@mui/material";
import { Instagram, Facebook, YouTube } from "@mui/icons-material";
import { Link as RouterLink, useNavigate } from "react-router-dom";

const Footer = ({ activeButton, handleNavigation }) => {
  const navigate = useNavigate();

  const handleClick = (path) => {
    handleNavigation(path);
    navigate(path);
  };

  return (
    <Box component="footer" sx={{ bgcolor: "#0a2243", color: "white", mt: 0, mb: 0 }}>
      <Container className="main">
        <Grid
          container
          spacing={2}
          sx={{ padding: 3 }}
          justifyContent={"center"}
        >
          <Grid item xs={12} sm={4} lg={5}>
            <Typography variant="h6">Information</Typography>
            <ul style={{ listStyleType: "none", padding: 0 }}>
              <li>
                <RouterLink
                  to="/privacy-policy"
                  style={{ color: "inherit", textDecoration: "none" }}
                >
                  Privacy policy
                </RouterLink>
              </li>
              <li>
                <RouterLink
                  to="/terms-and-conditions"
                  style={{ color: "inherit", textDecoration: "none" }}
                >
                  Terms & conditions
                </RouterLink>
              </li>
            </ul>
          </Grid>
          <Grid item xs={12} sm={4} lg={4}>
            <Typography variant="h6">Quick Link</Typography>
            <ul style={{ listStyleType: "none", padding: 0 }}>
              <li>
                <RouterLink
                  to="/"
                  onClick={() => handleClick("/")}
                  style={{ color: "inherit", textDecoration: "none" }}
                >
                  Home
                </RouterLink>
              </li>
              <li>
                <RouterLink
                  to="/jobs"
                  onClick={() => handleClick("/jobs")}
                  style={{ color: "inherit", textDecoration: "none" }}
                >
                  Jobs
                </RouterLink>
              </li>
              <li>
                <RouterLink
                  to="/about"
                  onClick={() => handleClick("/about-us")}
                  style={{ color: "inherit", textDecoration: "none" }}
                >
                  About us
                </RouterLink>
              </li>
              <li>
                <RouterLink
                  to="/contact"
                  onClick={() => handleClick("/contact-us")}
                  style={{ color: "inherit", textDecoration: "none" }}
                >
                  Contact us
                </RouterLink>
              </li>
            </ul>
          </Grid>
          <Grid item xs={12} sm={4} lg={3}>
            <Typography variant="h6">Address</Typography>
            <Typography variant="body1">
              VIENSTEREOPTIC,grow@vienstereoptic.com
              <br />
              +91 9176176738
              <br />
              2F/993 P &T Colony 5th street (west), Tuticorin 628008
            </Typography>
          </Grid>
        </Grid>

        <Grid container spacing={3} justifyContent="center" alignItems="center">
          <Grid item>
            <Typography variant="body2" color="white">
              &copy; 2025 VIENSTEREOPTIC HRMS. All rights reserved.
            </Typography>
          </Grid>
          <Grid item>
            <IconButton
              href="#"
              target="_blank"
            >
              <Instagram sx={{ color: "white" }} />
            </IconButton>
            <IconButton
              href="#"
              target="_blank"
            >
              <Facebook sx={{ color: "white" }} />
            </IconButton>
            <IconButton
              href="#"
              target="_blank"
            >
              <YouTube sx={{ color: "white" }} />
            </IconButton>
          </Grid>
        </Grid>
      </Container>
    </Box>
  );
};

export default Footer;
