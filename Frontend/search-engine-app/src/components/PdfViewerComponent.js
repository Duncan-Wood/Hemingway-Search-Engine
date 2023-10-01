import React, { useEffect, useRef, useCallback } from "react";

// PdfViewerComponent is a React component for rendering a PDF viewer using PSPDFKit.
// It dynamically loads PSPDFKit when mounted and unloads it when unmounted.
// using a Ref is a way to manipulate the DOM directly and avoid React's rerendering
export default function PdfViewerComponent(props) {
  // Create a reference to the container div where PSPDFKit will be rendered.
  const containerRef = useRef(null);
  // Create a reference to store the PSPDFKit instance.
  const PSPDFKitRef = useRef(null);

  // Initialize the PDF viewer using PSPDFKit when the component is mounted or when props.document changes.
  const initializePdfViewer = useCallback(async () => {
    const container = containerRef.current;

    try {
      // Dynamically import PSPDFKit library.
      const PSPDFKit = await import("pspdfkit");

      if (PSPDFKit && container) {
        // Store the PSPDFKit instance in a ref for later use.
        PSPDFKitRef.current = PSPDFKit;

        // Unload any existing PSPDFKit instance from the container.
        PSPDFKit.unload(container);

        // Load the PDF document into the container.
        await PSPDFKit.load({
          container,
          document: props.document,
          baseUrl: `${window.location.protocol}//${window.location.host}/${process.env.PUBLIC_URL}`,
        });
      }
    } catch (error) {
      console.error("Error loading PSPDFKit:", error);
    }
  }, [props.document]);

  // Cleanup function to unload PSPDFKit when the component is unmounted.
  useEffect(() => {
    const cleanupPdfViewer = () => {
      const container = containerRef.current;
      const PSPDFKit = PSPDFKitRef.current;

      if (container && PSPDFKit) {
        try {
          // Unload PSPDFKit from the container to release resources.
          PSPDFKit.unload(container);
        } catch (error) {
          console.error("Error unloading PSPDFKit:", error);
        }
      }
    };

    // Initialize the PDF viewer when the component mounts.
    initializePdfViewer();

    // Return the cleanup function to be executed when the component unmounts.
    return cleanupPdfViewer;
  }, [initializePdfViewer]);

  // Render a div with a ref for PSPDFKit container and set its width and height.
  return <div ref={containerRef} style={{ width: "100%", height: "100vh" }} />;
}
