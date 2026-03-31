export default function AdminPage() {
  return (
    <section>
      <h2 style={{ marginTop: 0 }}>Admin Tools</h2>

      <div
        style={{
          display: "grid",
          gap: 16,
        }}
      >
        <div style={panelStyle}>
          <h3 style={{ marginTop: 0 }}>Links</h3>
          <ul>
            <li>
              <a href="http://localhost:8000/admin/" target="_blank" rel="noreferrer">
                Django Admin
              </a>
            </li>
            <li>
              <a href="http://localhost:8000/api/docs/" target="_blank" rel="noreferrer">
                API Docs
              </a>
            </li>
          </ul>
        </div>

        <div style={panelStyle}>
          <h3 style={{ marginTop: 0 }}>Replay Comparison Script</h3>
          <pre style={preStyle}>python ..\infra\scripts\replay_comparison.py --run-id 1</pre>
        </div>

        <div style={panelStyle}>
          <h3 style={{ marginTop: 0 }}>Run Eval Suite</h3>
          <pre style={preStyle}>python ..\infra\scripts\generate_eval_cases.py{"\n"}python ..\infra\scripts\run_eval_suite.py</pre>
        </div>
      </div>
    </section>
  );
}

const panelStyle: React.CSSProperties = {
  backgroundColor: "#ffffff",
  border: "1px solid #e2e8f0",
  borderRadius: 12,
  padding: 16,
};

const preStyle: React.CSSProperties = {
  backgroundColor: "#f8fafc",
  border: "1px solid #e2e8f0",
  borderRadius: 8,
  padding: 12,
  overflowX: "auto",
};