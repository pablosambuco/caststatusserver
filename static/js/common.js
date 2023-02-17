var Console = {
  log(message) {
    console.log(message);
  },
};

function escapeHTML(unsafe) {
  if (typeof unsafe === "string" || unsafe instanceof String)
  {
    return unsafe
      .replaceAll("&", "&amp;")
      .replaceAll("<", "&lt;")
      .replaceAll(">", "&gt;")
      .replaceAll('"', "&quot;")
      .replaceAll("'", "&#039;");
  }
  return unsafe;
}
