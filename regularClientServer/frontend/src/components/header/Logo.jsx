import React from "react";
import { makeStyles } from "@material-ui/core/styles";
import Toolbar from "@material-ui/core/Toolbar";
import Typography from "@material-ui/core/Typography";

const useStyles = makeStyles((theme) => ({
  toolbar: {
    borderBottom: `1px solid ${theme.palette.divider}`,
  },
  toolbarTitle: {
    flex: 1,
  },
}));

export default function Logo() {
  const classes = useStyles();

  return (
    <Toolbar className={classes.toolbar}>
      <Typography
        style={{ fontFamily: "vogue", fontSize: "11rem" }}
        component="h1"
        variant="h1"
        color="initial"
        align="center"
        noWrap
        className={classes.toolbarTitle}
      >
        STAR WARS
      </Typography>
    </Toolbar>
  );
}