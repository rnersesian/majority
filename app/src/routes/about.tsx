import { Title } from "@solidjs/meta";
import { useLocation } from "@solidjs/router";

export default function Home() {

  const location = useLocation()

  

  return (
    <main>
      <Title>About</Title>
      <h1>About</h1>
    </main>
  );
}
