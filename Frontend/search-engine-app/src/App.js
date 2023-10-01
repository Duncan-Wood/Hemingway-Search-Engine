import React, { useState } from "react";
import "./App.css";

import NavigationMenuClosed from "./components/NavigationMenuClosed";
import NavigationMenuOpen from "./components/NavigationMenuOpen";
import PdfViewerComponent from "./components/PdfViewerComponent";

const App = () => {
  // State to track whether the navigation menu is expanded or not.
  const [menuExpanded, setMenuExpanded] = useState(false);

  // Function to toggle the menuExpanded state.
  const toggleMenu = () => {
    setMenuExpanded(!menuExpanded);
  };

  return (
    <div className="app">
      {/* Render the closed navigation menu with a click handler */}
      <NavigationMenuClosed onClick={toggleMenu} />

      {/* Conditionally render the open navigation menu if menuExpanded is true */}
      {menuExpanded && <NavigationMenuOpen onClose={toggleMenu} />}

      <div className="PDF-viewer">
        {/* Render the PDF viewer component with a document prop */}
        <PdfViewerComponent document={"hemingway.pdf"} />
      </div>
    </div>
  );
};

export default App;
