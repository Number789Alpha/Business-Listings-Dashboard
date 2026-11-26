
import { useEffect, useState } from "react";
import axios from "axios";
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip,
  ResponsiveContainer, PieChart, Pie, Cell, Legend
} from "recharts";
import {
  LayoutDashboard, Building2, MapPin, Tags, Database,
  RefreshCw, TrendingUp, Search, Menu
} from "lucide-react";
import "./App.css";

const API = "http://127.0.0.1:8000";

const COLORS = [
  "#6366f1", "#06b6d4", "#f59e0b", "#10b981",
  "#ec4899", "#8b5cf6", "#f97316", "#14b8a6"
];

function App() {
  const [summary, setSummary] = useState(null);
  const [cities, setCities] = useState([]);
  const [categories, setCategories] = useState([]);
  const [sources, setSources] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const fetchDashboardData = async () => {
    try {
      setLoading(true);
      setError("");

      const [summaryRes, citiesRes, categoriesRes, sourcesRes] =
        await Promise.all([
          axios.get(`${API}/api/summary`),
          axios.get(`${API}/api/cities`),
          axios.get(`${API}/api/categories`),
          axios.get(`${API}/api/sources`)
        ]);

      setSummary(summaryRes.data);
      setCities(citiesRes.data);
      setCategories(categoriesRes.data);
      setSources(sourcesRes.data);
    } catch (err) {
      console.error("Dashboard API error:", err);
      setError("Unable to fetch dashboard data. Check your backend.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const topCategories = categories.slice(0, 8);

  const cards = [
    {
      title: "Total Businesses",
      value: summary?.total_businesses ?? 0,
      icon: Building2,
      color: "purple"
    },
    {
      title: "Total Cities",
      value: summary?.total_cities ?? 0,
      icon: MapPin,
      color: "blue"
    },
    {
      title: "Total Categories",
      value: summary?.total_categories ?? 0,
      icon: Tags,
      color: "orange"
    },
    {
      title: "Data Sources",
      value: summary?.total_sources ?? 0,
      icon: Database,
      color: "green"
    }
  ];

  return (
    <div className="dashboard">

      <aside className="sidebar">
        <div className="brand">
          <div className="brand-icon"><Building2 size={25} /></div>
          <div>
            <h2>BizAnalytics</h2>
            <span>Business Intelligence</span>
          </div>
        </div>

        <div className="nav-label">MAIN MENU</div>

        <nav>
          <a className="nav-item active" href="#dashboard">
            <LayoutDashboard size={19} /> Dashboard
          </a>
          <a className="nav-item" href="#analytics">
            <TrendingUp size={19} /> Analytics
          </a>
          <a className="nav-item" href="#listings">
            <Building2 size={19} /> Listings Overview
          </a>
        </nav>

        <div className="sidebar-bottom">
          <div className="status-dot"></div>
          <span>Database Connected</span>
        </div>
      </aside>

      <main className="main-content">

        <header className="topbar">
          <div>
            <h1>Business Dashboard</h1>
            <p>Monitor and analyze your business listings</p>
          </div>

          <button className="refresh-btn" onClick={fetchDashboardData}>
            <RefreshCw size={16} />
            Refresh Data
          </button>
        </header>

        {error && <div className="error-message">{error}</div>}

        {loading ? (
          <div className="loading">Loading dashboard data...</div>
        ) : (
          <>
            <section className="welcome-section">
              <div>
                <h2>Overview</h2>
                <p>Here's what's happening with your business data.</p>
              </div>
              <span className="live-badge">● LIVE DATA</span>
            </section>

            <section className="stats-grid">
              {cards.map((card) => {
                const Icon = card.icon;

                return (
                  <div className="stat-card" key={card.title}>
                    <div className={`stat-icon ${card.color}`}>
                      <Icon size={23} />
                    </div>
                    <div className="stat-info">
                      <p>{card.title}</p>
                      <h2>{card.value.toLocaleString("en-IN")}</h2>
                    </div>
                  </div>
                );
              })}
            </section>

            <section className="charts-grid" id="analytics">

              <div className="chart-card">
                <div className="chart-heading">
                  <div>
                    <h3>City-wise Distribution</h3>
                    <p>Business listings across cities</p>
                  </div>
                  <MapPin size={20} />
                </div>

                <ResponsiveContainer width="100%" height={300}>
                  <BarChart data={cities} margin={{ top: 15, right: 15, left: 0, bottom: 5 }}>
                    <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e8eaf0" />
                    <XAxis dataKey="city" axisLine={false} tickLine={false} />
                    <YAxis axisLine={false} tickLine={false} />
                    <Tooltip />
                    <Bar dataKey="total_businesses" fill="#6366f1" radius={[7, 7, 0, 0]} />
                  </BarChart>
                </ResponsiveContainer>
              </div>

              <div className="chart-card">
                <div className="chart-heading">
                  <div>
                    <h3>Top Categories</h3>
                    <p>Distribution by business category</p>
                  </div>
                  <Tags size={20} />
                </div>

                <ResponsiveContainer width="100%" height={300}>
                  <PieChart>
                    <Pie
                      data={topCategories}
                      dataKey="total_businesses"
                      nameKey="category"
                      cx="50%"
                      cy="45%"
                      innerRadius={65}
                      outerRadius={105}
                      paddingAngle={3}
                    >
                      {topCategories.map((item, index) => (
                        <Cell key={item.category} fill={COLORS[index % COLORS.length]} />
                      ))}
                    </Pie>
                    <Tooltip />
                    <Legend />
                  </PieChart>
                </ResponsiveContainer>
              </div>
            </section>

            <section className="bottom-grid" id="listings">

              <div className="chart-card">
                <div className="chart-heading">
                  <div>
                    <h3>Category Breakdown</h3>
                    <p>Top business categories by record count</p>
                  </div>
                  <Search size={20} />
                </div>

                <div className="category-list">
                  {topCategories.map((item, index) => (
                    <div className="category-row" key={item.category}>
                      <div className="category-name">
                        <span
                          className="category-dot"
                          style={{ background: COLORS[index % COLORS.length] }}
                        />
                        <span>{item.category}</span>
                      </div>
                      <strong>{item.total_businesses.toLocaleString("en-IN")}</strong>
                    </div>
                  ))}
                </div>
              </div>

              <div className="chart-card">
                <div className="chart-heading">
                  <div>
                    <h3>Data Sources</h3>
                    <p>Records collected from each source</p>
                  </div>
                  <Database size={20} />
                </div>

                <div className="source-list">
                  {sources.map((item) => (
                    <div className="source-item" key={item.source}>
                      <div>
                        <div className="source-name">{item.source}</div>
                        <div className="source-bar">
                          <div
                            className="source-fill"
                            style={{
                              width: `${summary.total_businesses
                                ? (item.total_businesses / summary.total_businesses) * 100
                                : 0}%`
                            }}
                          />
                        </div>
                      </div>
                      <strong>{item.total_businesses.toLocaleString("en-IN")}</strong>
                    </div>
                  ))}
                </div>
              </div>

            </section>
          </>
        )}

        <footer>
          Business Listings Analytics Dashboard · Powered by React, FastAPI & MySQL
        </footer>

      </main>
    </div>
  );
}

export default App;
