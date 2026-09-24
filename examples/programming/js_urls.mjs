const u = new URL("https://lab.test:8443/help");
u.searchParams.set("q", "hello lab");
console.log(u.origin, u.pathname);
console.log(u.href);
