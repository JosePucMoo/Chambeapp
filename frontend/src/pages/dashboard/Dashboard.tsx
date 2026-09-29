import type { LayoutContextType } from "@/interfaces/Context";
import { useEffect } from "react";
import { useOutletContext } from "react-router-dom";

const Dashboard = () => {
  const { setPageTitle } = useOutletContext<LayoutContextType>();

  useEffect(() => {
    setPageTitle("Tablero");
  }, [setPageTitle]);
  return <div>dashboard</div>;
};

export default Dashboard;
