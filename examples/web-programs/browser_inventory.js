// Run in Developer Tools on your own training page. No requests or form submissions.
(() => {
  const summarize = value => {
    try {
      const u = new URL(value, document.baseURI);
      return {origin:u.origin, path:u.pathname, sameOrigin:u.origin===location.origin};
    } catch {return {invalid:true};}
  };
  const links = [...document.querySelectorAll("a[href]")].map(a => summarize(a.getAttribute("href")));
  const forms = [...document.forms].map(form => ({
    method:form.method.toUpperCase(), destination:summarize(form.getAttribute("action") || location.href),
    fields:[...form.elements].filter(e=>e.name).map(e=>({name:e.name,type:e.type}))
  }));
  console.log({links, forms, note:"Query strings, fragments and field values omitted. Paths and field names can still be sensitive. Hidden fields do not establish CSRF protection."});
})();
