import React from "react";
import Container from "@material-ui/core/Container";
import Logo from "./Logo";

export default function Header(props) {
  return (
    <React.Fragment>
      <Container maxWidth="xlg">
        <Logo />
      </Container>
    </React.Fragment>
  );
}