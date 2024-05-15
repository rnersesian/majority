import { MetaProvider, Title } from "@solidjs/meta";
import { Router } from "@solidjs/router";
import { FileRoutes } from "@solidjs/start/router";
import { Suspense } from "solid-js";
import "./style/app.css"


export default function App() {
  return (
    <Router
      root={props => (
        <MetaProvider>
          <Title>SolidStart - Basic</Title>
          <div id="top-navbar">
            <a href="/">Home</a>
            <a href="/about">About</a>
            <a href="/help">help</a>
          </div>
          <Suspense>{props.children}</Suspense> 
        </MetaProvider>
      )}
    >
      <FileRoutes />
    </Router>
  );
}
