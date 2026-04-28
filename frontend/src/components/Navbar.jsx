export default function Navbar() {
  const handleLogout = () => {
    localStorage.removeItem("token");
    window.location.href = "/";
  };

  return (
    <div
      style={{
        display: "flex",
        justifyContent: "space-between",
        padding: "15px 30px",
        backgroundColor: "#f5f5f5",
        borderBottom: "1px solid #ddd",
      }}
    >
      <div>
        <strong>Mental Health App</strong>
      </div>

      <div>
        <button onClick={() => (window.location.href = "/dashboard")}>
          Dashboard
        </button>

        <button
          onClick={() => (window.location.href = "/history")}
          style={{ marginLeft: "10px" }}
        >
          History
        </button>

        <button
          onClick={handleLogout}
          style={{ marginLeft: "10px" }}
        >
          Logout
        </button>
      </div>
    </div>
  );
}