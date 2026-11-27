import { useEffect, useState } from "react";
import axios from "axios";

import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  Legend
} from "recharts";

import {
  LayoutDashboard,
  Building2,
  MapPin,
  Tags,
  Database,
  RefreshCw,
  TrendingUp,
  Search,
  Map,
  Filter,
  Download
} from "lucide-react";

import "./App.css";

const API = "https://business-listings-dashboard-53i6.onrender.com";

const COLORS = [
  "#6366f1",
  "#06b6d4",
  "#f59e0b",
  "#10b981",
  "#ec4899",
  "#8b5cf6",
  "#f97316",
  "#14b8a6"
];

function App() {
  // Dashboard data
  const [summary, setSummary] = useState(null);
  const [cities, setCities] = useState([]);
  const [categories, setCategories] = useState([]);
  const [sources, setSources] = useState([]);

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  // India-wide filter data
  const [indiaStates, setIndiaStates] = useState([]);
  const [stateSummary, setStateSummary] = useState([]);
  const [districts, setDistricts] = useState([]);

  const [selectedState, setSelectedState] = useState("");
  const [selectedDistrict, setSelectedDistrict] = useState("");

  const [indiaLoading, setIndiaLoading] = useState(true);
  const [indiaError, setIndiaError] = useState("");

  // Business listings table state
  const [listings, setListings] = useState([]);
  const [listingsTotal, setListingsTotal] = useState(0);
  const [listingsPage, setListingsPage] = useState(1);
  const [listingsPages, setListingsPages] = useState(0);
  const [listingsSearch, setListingsSearch] = useState("");
  const [listingsCategory, setListingsCategory] = useState("");
  const [listingsSortBy, setListingsSortBy] = useState("business_name");
  const [listingsSortOrder, setListingsSortOrder] = useState("asc");
  const [listingsLoading, setListingsLoading] = useState(false);
  const [listingsError, setListingsError] = useState("");

  // Fetch filtered dashboard data
  const fetchDashboardData = async (state, district) => {
    if (!state) return;

    try {
      setLoading(true);
      setError("");

      const params = {
        state,
        ...(district ? { district } : {})
      };

      const [
        summaryRes,
        citiesRes,
        categoriesRes,
        sourcesRes
      ] = await Promise.all([
        axios.get(`${API}/api/india/summary`, { params }),
        axios.get(`${API}/api/india/cities`, { params }),
        axios.get(`${API}/api/india/categories`, { params }),
        axios.get(`${API}/api/india/sources`, { params })
      ]);

      setSummary(summaryRes.data);
      setCities(citiesRes.data);
      setCategories(categoriesRes.data);
      setSources(sourcesRes.data);

    } catch (err) {
      console.error("Filtered dashboard API error:", err);
      setError(
        "Unable to fetch filtered dashboard data. Check the backend."
      );
    } finally {
      setLoading(false);
    }
  };

  // Fetch all states and nationwide state comparison
  const fetchIndiaData = async () => {
    try {
      setIndiaLoading(true);
      setIndiaError("");

      const [statesRes, summaryRes] = await Promise.all([
        axios.get(`${API}/api/states`),
        axios.get(`${API}/api/state-summary`)
      ]);

      setIndiaStates(statesRes.data);
      setStateSummary(summaryRes.data);

      // Set Madhya Pradesh as the default state
      if (statesRes.data.length > 0) {
        setSelectedState((current) => {
          if (
            current &&
            statesRes.data.some((item) => item.state === current)
          ) {
            return current;
          }

          const mp = statesRes.data.find(
            (item) => item.state === "Madhya Pradesh"
          );

          return mp ? mp.state : statesRes.data[0].state;
        });
      }

    } catch (err) {
      console.error("India dashboard API error:", err);
      setIndiaError(
        "Unable to fetch India-wide dashboard data."
      );
    } finally {
      setIndiaLoading(false);
    }
  };

  // Fetch districts according to selected state
  const fetchDistricts = async (state) => {
    if (!state) {
      setDistricts([]);
      return;
    }

    try {
      const response = await axios.get(
        `${API}/api/districts`,
        {
          params: { state }
        }
      );

      setDistricts(response.data);

    } catch (err) {
      console.error("District API error:", err);
      setDistricts([]);
      setIndiaError("Unable to fetch district data.");
    }
  };

  // Fetch business listings using the current dashboard filters
  const fetchListings = async (
    state,
    district,
    page = listingsPage,
    search = listingsSearch,
    category = listingsCategory,
    sortBy = listingsSortBy,
    sortOrder = listingsSortOrder
  ) => {
    if (!state) return;

    try {
      setListingsLoading(true);
      setListingsError("");

      const response = await axios.get(`${API}/api/india/listings`, {
        params: {
          state,
          ...(district ? { district } : {}),
          ...(search.trim() ? { search: search.trim() } : {}),
          ...(category ? { category } : {}),
          page,
          limit: 25,
          sort_by: sortBy,
          sort_order: sortOrder
        }
      });

      setListings(response.data.data || []);
      setListingsTotal(response.data.total || 0);
      setListingsPages(response.data.total_pages || 0);
    } catch (err) {
      console.error("Business listings API error:", err);
      setListingsError("Unable to load business listings. Please try again.");
      setListings([]);
      setListingsTotal(0);
      setListingsPages(0);
    } finally {
      setListingsLoading(false);
    }
  };

  // Initial dashboard load
  useEffect(() => {
    fetchIndiaData();
  }, []);

  // Fetch districts whenever selected state changes
  useEffect(() => {
    if (selectedState) {
      fetchDistricts(selectedState);
    }
  }, [selectedState]);

  // Fetch dashboard data whenever state or district changes
  useEffect(() => {
    if (selectedState) {
      fetchDashboardData(
        selectedState,
        selectedDistrict
      );
    }
  }, [selectedState, selectedDistrict]);

  // Refresh business listings when filters, search, page or sorting change
  useEffect(() => {
    if (selectedState) {
      fetchListings(
        selectedState,
        selectedDistrict,
        listingsPage,
        listingsSearch,
        listingsCategory,
        listingsSortBy,
        listingsSortOrder
      );
    }
  }, [
    selectedState,
    selectedDistrict,
    listingsPage,
    listingsSearch,
    listingsCategory,
    listingsSortBy,
    listingsSortOrder
  ]);

  // Refresh dashboard data
  const handleRefresh = async () => {
    await fetchIndiaData();

    if (selectedState) {
      await fetchDistricts(selectedState);

      await fetchDashboardData(
        selectedState,
        selectedDistrict
      );
    }
  };
    // Export all filtered business listings to CSV
  const handleExportCSV = async () => {
    if (!selectedState) {
      alert("Please select a state first.");
      return;
    }

    try {
      setListingsLoading(true);

      const limit = 100;

      // Fetch first page to determine total pages
      const firstResponse = await axios.get(
        `${API}/api/india/listings`,
        {
          params: {
            state: selectedState,
            ...(selectedDistrict ? { district: selectedDistrict } : {}),
            ...(listingsSearch.trim()
              ? { search: listingsSearch.trim() }
              : {}),
            ...(listingsCategory ? { category: listingsCategory } : {}),
            page: 1,
            limit,
            sort_by: listingsSortBy,
            sort_order: listingsSortOrder
          }
        }
      );

      const allRecords = [...(firstResponse.data.data || [])];
      const totalPages = firstResponse.data.total_pages || 0;

      // Fetch remaining pages
      for (let page = 2; page <= totalPages; page++) {
        const response = await axios.get(
          `${API}/api/india/listings`,
          {
            params: {
              state: selectedState,
              ...(selectedDistrict ? { district: selectedDistrict } : {}),
              ...(listingsSearch.trim()
                ? { search: listingsSearch.trim() }
                : {}),
              ...(listingsCategory ? { category: listingsCategory } : {}),
              page,
              limit,
              sort_by: listingsSortBy,
              sort_order: listingsSortOrder
            }
          }
        );

        allRecords.push(...(response.data.data || []));
      }

      if (allRecords.length === 0) {
        alert("No records available to export.");
        return;
      }

      // CSV columns
      const columns = [
        "business_name",
        "category",
        "state",
        "district",
        "city",
        "address",
        "phone",
        "source"
      ];

      // Escape CSV values safely
      const escapeCSV = (value) => {
        let text = String(value ?? "");

        // Protect against spreadsheet formula injection
        if (/^[\s]*[=+\-@]/.test(text)) {
          text = "'" + text;
        }

        return `"${text.replace(/"/g, '""')}"`;
      };

      const csvRows = [
        columns.join(","),
        ...allRecords.map((record) =>
          columns
            .map((column) => escapeCSV(record[column]))
            .join(",")
        )
      ];

      const csvContent = "\uFEFF" + csvRows.join("\n");

      const blob = new Blob(
        [csvContent],
        { type: "text/csv;charset=utf-8;" }
      );

      const url = URL.createObjectURL(blob);
      const link = document.createElement("a");

      link.href = url;
      link.download = `business_listings_${selectedState.replace(/\s+/g, "_")}.csv`;

      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);

      URL.revokeObjectURL(url);

      alert(`${allRecords.length.toLocaleString("en-IN")} records exported successfully!`);

    } catch (err) {
      console.error("CSV export error:", err);
      alert("Unable to export CSV. Please check the backend.");
    } finally {
      setListingsLoading(false);
    }
  };

  // Get top 8 categories
  const topCategories = categories.slice(0, 8);

  // KPI cards
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
      value: summary?.total_sources ?? sources.length,
      icon: Database,
      color: "green"
    }
  ];

  // Calculate total listings across India
  const totalIndiaListings = indiaStates.reduce(
    (total, item) =>
      total + Number(item.total_businesses || 0),
    0
  );

  // Get selected state summary
  const selectedStateSummary = stateSummary.find(
    (item) => item.state === selectedState
  );

  // Get district chart data
  const filteredDistricts = selectedDistrict
    ? districts.filter(
        (item) => item.district === selectedDistrict
      )
    : [...districts]
        .sort(
          (a, b) =>
            Number(b.total_businesses) -
            Number(a.total_businesses)
        )
        .slice(0, 10);

  return (
    <div className="dashboard">

      {/* SIDEBAR */}
      <aside className="sidebar">

        <div className="brand">
          <div className="brand-icon">
            <Building2 size={25} />
          </div>

          <div>
            <h2>BizAnalytics</h2>
            <span>Business Intelligence</span>
          </div>
        </div>

        <div className="nav-label">
          MAIN MENU
        </div>

        <nav>
          <a
            className="nav-item active"
            href="#dashboard"
          >
            <LayoutDashboard size={19} />
            Dashboard
          </a>

          <a
            className="nav-item"
            href="#analytics"
          >
            <TrendingUp size={19} />
            Analytics
          </a>

          <a
            className="nav-item"
            href="#business-listings"
          >
            <Building2 size={19} />
            Listings Overview
          </a>

          <a
            className="nav-item"
            href="#india-analytics"
          >
            <Map size={19} />
            India Analytics
          </a>
        </nav>

        <div className="sidebar-bottom">
          <div className="status-dot"></div>
          <span>Database Connected</span>
        </div>

      </aside>

      {/* MAIN CONTENT */}
      <main className="main-content">

        {/* TOPBAR */}
        <header className="topbar">

          <div>
            <h1>Business Dashboard</h1>
            <p>
              Monitor and analyze your business listings
            </p>
          </div>

          <button
            className="refresh-btn"
            onClick={handleRefresh}
          >
            <RefreshCw size={16} />
            Refresh Data
          </button>

        </header>
                {/* ERROR MESSAGE */}
        {error && (
          <div className="error-message">
            {error}
          </div>
        )}

        {/* LOADING OR DASHBOARD */}
        {loading ? (
          <div className="loading">
            Loading dashboard data...
          </div>
        ) : (
          <>

            {/* OVERVIEW */}
            <section
              className="welcome-section"
              id="dashboard"
            >

              <div>
                <h2>Overview</h2>
                <p>
                  Here's what's happening with your selected business data.
                </p>
              </div>

              <span className="live-badge">
                ● LIVE DATA
              </span>

            </section>

            {/* FILTERED KPI CARDS */}
            <section className="stats-grid">

              {cards.map((card) => {
                const Icon = card.icon;

                return (
                  <div
                    className="stat-card"
                    key={card.title}
                  >

                    <div
                      className={`stat-icon ${card.color}`}
                    >
                      <Icon size={23} />
                    </div>

                    <div className="stat-info">

                      <p>{card.title}</p>

                      <h2>
                        {Number(card.value).toLocaleString("en-IN")}
                      </h2>

                    </div>

                  </div>
                );
              })}

            </section>

            {/* INDIA-WIDE ANALYTICS */}
            <section
              className="india-section"
              id="india-analytics"
            >

              <div className="india-heading">

                <div>
                  <h2>
                    India-Wide Business Analytics
                  </h2>

                  <p>
                    Explore collected business listings across 28 Indian states
                  </p>
                </div>

                <span className="india-badge">
                  <Map size={15} />
                  INDIA DATA
                </span>

              </div>

              {/* INDIA DATA LOADING */}
              {indiaLoading ? (
                <div className="loading">
                  Loading India-wide data...
                </div>
              ) : indiaError ? (
                <div className="error-message">
                  {indiaError}
                </div>
              ) : (
                <>

                  {/* INDIA STATISTICS */}
                  <div className="india-stats">

                    <div className="india-stat-card">
                      <span>
                        Total India Listings (all states)
                      </span>

                      <h2>
                        {totalIndiaListings.toLocaleString("en-IN")}
                      </h2>
                    </div>

                    <div className="india-stat-card">
                      <span>States Covered</span>

                      <h2>
                        {indiaStates.length}
                      </h2>
                    </div>

                    <div className="india-stat-card">
                      <span>Selected State</span>

                      <h2>
                        {selectedState || "—"}
                      </h2>
                    </div>

                    <div className="india-stat-card">
                      <span>
                        Districts with Listings
                      </span>

                      <h2>
                        {
                          selectedDistrict
                            ? 1
                            : (
                                selectedStateSummary?.total_districts ?? 0
                              )
                        }
                      </h2>
                    </div>

                  </div>

                  {/* STATE AND DISTRICT FILTERS */}
                  <div className="india-filters">

                    {/* STATE FILTER */}
                    <div className="filter-group">

                      <label htmlFor="state-filter">
                        <Map size={16} />
                        Select State
                      </label>

                      <select
                        id="state-filter"
                        value={selectedState}
                        onChange={(e) => {
                          setSelectedState(e.target.value);
                          setSelectedDistrict("");
                        }}
                      >

                        {indiaStates.map((item) => (
                          <option
                            key={item.state}
                            value={item.state}
                          >
                            {item.state}
                          </option>
                        ))}

                      </select>

                    </div>

                    {/* DISTRICT FILTER */}
                    <div className="filter-group">

                      <label htmlFor="district-filter">
                        <Filter size={16} />
                        Select District
                      </label>

                      <select
                        id="district-filter"
                        value={selectedDistrict}
                        onChange={(e) =>
                          setSelectedDistrict(e.target.value)
                        }
                        disabled={!districts.length}
                      >

                        <option value="">
                          All Districts
                        </option>

                        {districts.map((item) => (
                          <option
                            key={item.district}
                            value={item.district}
                          >
                            {item.district}
                          </option>
                        ))}

                      </select>

                    </div>

                  </div>

                  {/* STATE-WISE ANALYTICS */}
                  <div className="india-chart-card">

                    <div className="chart-heading">

                      <div>
                        <h3>District-wise Business Listings</h3>

                        <p>
                          {selectedDistrict
                            ? `Showing ${selectedDistrict}`
                            : `Top districts in ${selectedState}`}
                        </p>
                      </div>

                      <MapPin size={20} />

                    </div>

                    <div className="chart-container">

                      <ResponsiveContainer
                        width="100%"
                        height={320}
                      >

                        <BarChart
                          data={filteredDistricts}
                          margin={{
                            top: 10,
                            right: 20,
                            left: 10,
                            bottom: 55
                          }}
                        >

                          <CartesianGrid
                            strokeDasharray="3 3"
                            vertical={false}
                          />

                          <XAxis
                            dataKey="district"
                            angle={-35}
                            textAnchor="end"
                            interval={0}
                            height={75}
                            tick={{ fontSize: 11 }}
                          />

                          <YAxis />

                          <Tooltip />

                          <Bar
                            dataKey="total_businesses"
                            name="Businesses"
                            fill="#6366f1"
                            radius={[5, 5, 0, 0]}
                          />

                        </BarChart>

                      </ResponsiveContainer>

                    </div>

                  </div>

                  {/* STATE-WISE COMPARISON */}
                  <div className="india-chart-card">

                    <div className="chart-heading">

                      <div>
                        <h3>State-wise Business Comparison</h3>

                        <p>
                          Business listings across all available states
                        </p>
                      </div>

                      <TrendingUp size={20} />

                    </div>

                    <div className="chart-container">

                      <ResponsiveContainer
                        width="100%"
                        height={380}
                      >

                        <BarChart
                          data={stateSummary}
                          margin={{
                            top: 10,
                            right: 20,
                            left: 10,
                            bottom: 100
                          }}
                        >

                          <CartesianGrid
                            strokeDasharray="3 3"
                            vertical={false}
                          />

                          <XAxis
                            dataKey="state"
                            angle={-45}
                            textAnchor="end"
                            interval={0}
                            height={110}
                            tick={{ fontSize: 10 }}
                          />

                          <YAxis />

                          <Tooltip />

                          <Bar
                            dataKey="total_businesses"
                            name="Businesses"
                            fill="#06b6d4"
                            radius={[5, 5, 0, 0]}
                          />

                        </BarChart>

                      </ResponsiveContainer>

                    </div>

                  </div>

                </>
              )}

            </section>

            {/* ANALYTICS SECTION */}
            <section
              className="analytics-section"
              id="analytics"
            >

              <div className="section-heading">

                <div>
                  <h2>Business Analytics</h2>

                  <p>
                    Detailed analysis of {selectedDistrict || selectedState}
                  </p>
                </div>

              </div>

              {/* CITY-WISE BUSINESS CHART */}
              <div className="chart-card">

                <div className="chart-heading">

                  <div>
                    <h3>City-wise Business Listings</h3>

                    <p>
                      Top cities based on collected listings
                    </p>
                  </div>

                  <MapPin size={20} />

                </div>

                <div className="chart-container">

                  <ResponsiveContainer
                    width="100%"
                    height={320}
                  >

                    <BarChart
                      data={cities.slice(0, 10)}
                      margin={{
                        top: 10,
                        right: 20,
                        left: 10,
                        bottom: 55
                      }}
                    >

                      <CartesianGrid
                        strokeDasharray="3 3"
                        vertical={false}
                      />

                      <XAxis
                        dataKey="city"
                        angle={-35}
                        textAnchor="end"
                        interval={0}
                        height={75}
                        tick={{ fontSize: 11 }}
                      />

                      <YAxis />

                      <Tooltip />

                      <Bar
                        dataKey="total_businesses"
                        name="Businesses"
                        fill="#8b5cf6"
                        radius={[5, 5, 0, 0]}
                      />

                    </BarChart>

                  </ResponsiveContainer>

                </div>

              </div>

              {/* CATEGORY PIE CHART */}
              <div className="chart-card">

                <div className="chart-heading">

                  <div>
                    <h3>Category Distribution</h3>

                    <p>
                      Business category share in {selectedDistrict || selectedState}
                    </p>
                  </div>

                  <Tags size={20} />

                </div>

                <div className="chart-container">

                  <ResponsiveContainer
                    width="100%"
                    height={320}
                  >

                    <PieChart>

                      <Pie
                        data={topCategories}
                        dataKey="total_businesses"
                        nameKey="category"
                        cx="50%"
                        cy="50%"
                        outerRadius={105}
                        label
                      >

                        {topCategories.map((item, index) => (
                          <Cell
                            key={item.category}
                            fill={COLORS[index % COLORS.length]}
                          />
                        ))}

                      </Pie>

                      <Tooltip />
                      <Legend />

                    </PieChart>

                  </ResponsiveContainer>

                </div>

              </div>

            </section>

            {/* CATEGORY BREAKDOWN AND DATA SOURCES */}
            <section
              className="bottom-grid"
              id="listings"
            >

              {/* CATEGORY BREAKDOWN */}
              <div className="chart-card">

                <div className="chart-heading">

                  <div>
                    <h3>Category Breakdown</h3>

                    <p>
                      Top categories in {selectedDistrict || selectedState}
                    </p>
                  </div>

                  <Search size={20} />

                </div>

                <div className="category-list">

                  {topCategories.map((item, index) => (

                    <div
                      className="category-row"
                      key={item.category}
                    >

                      <div className="category-name">

                        <span
                          className="category-dot"
                          style={{
                            background: COLORS[index % COLORS.length]
                          }}
                        />

                        <span>
                          {item.category}
                        </span>

                      </div>

                      <strong>
                        {Number(
                          item.total_businesses
                        ).toLocaleString("en-IN")}
                      </strong>

                    </div>

                  ))}

                </div>

              </div>

              {/* DATA SOURCES */}
              <div className="chart-card">

                <div className="chart-heading">

                  <div>
                    <h3>Data Sources</h3>

                    <p>
                      Records collected in {selectedDistrict || selectedState}
                    </p>
                  </div>

                  <Database size={20} />

                </div>

                <div className="source-list">

                  {sources.map((item) => (

                    <div
                      className="source-item"
                      key={item.source}
                    >

                      <div>

                        <div className="source-name">
                          {item.source}
                        </div>

                        <div className="source-bar">

                          <div
                            className="source-fill"
                            style={{
                              width: `${
                                summary?.total_businesses
                                  ? (
                                      item.total_businesses /
                                      summary.total_businesses
                                    ) * 100
                                  : 0
                              }%`
                            }}
                          />

                        </div>

                      </div>

                      <strong>
                        {Number(
                          item.total_businesses
                        ).toLocaleString("en-IN")}
                      </strong>

                    </div>

                  ))}

                </div>

              </div>

            </section>
                      </>
        )}

        {/* BUSINESS LISTINGS TABLE */}
        <section className="chart-card business-listings-section" id="business-listings">
          <div className="chart-heading">
            <div>
              <h3>Business Listings</h3>
              <p>
                Browse {Number(listingsTotal).toLocaleString("en-IN")} collected
                businesses in {selectedDistrict || selectedState || "India"}
              </p>
            </div>
            <Building2 size={20} />
          </div>

          <div className="listings-controls">
            <div className="listings-search">
              <Search size={17} />
              <input
                type="text"
                value={listingsSearch}
                placeholder="Search business name..."
                onChange={(e) => {
                  setListingsSearch(e.target.value);
                  setListingsPage(1);
                }}
              />
            </div>

            <select
              value={listingsCategory}
              onChange={(e) => {
                setListingsCategory(e.target.value);
                setListingsPage(1);
              }}
              aria-label="Filter listings by category"
            >
              <option value="">All Categories</option>
              {categories.map((item) => (
                <option key={item.category} value={item.category}>
                  {item.category}
                </option>
              ))}
            </select>

            <select
              value={listingsSortBy}
              onChange={(e) => {
                setListingsSortBy(e.target.value);
                setListingsPage(1);
              }}
              aria-label="Sort listings by"
            >
              <option value="business_name">Business Name</option>
              <option value="category">Category</option>
              <option value="city">City</option>
              <option value="district">District</option>
              <option value="state">State</option>
            </select>

            <select
              value={listingsSortOrder}
              onChange={(e) => {
                setListingsSortOrder(e.target.value);
                setListingsPage(1);
              }}
              aria-label="Sort order"
            >
              <option value="asc">Ascending</option>
              <option value="desc">Descending</option>
            </select>

            <button
              type="button"
              className="refresh-btn"
              onClick={() => {
                setListingsSearch("");
                setListingsCategory("");
                setListingsSortBy("business_name");
                setListingsSortOrder("asc");
                setListingsPage(1);
              }}
            >
              Reset
            </button>
            <button
  type="button"
  className="export-btn"
  onClick={handleExportCSV}
  disabled={listingsLoading}
>
  <Download size={16} />
  Export CSV
</button>
          </div>

          {listingsError && (
            <div className="error-message">{listingsError}</div>
          )}

          {listingsLoading ? (
            <div className="loading">Loading business listings...</div>
          ) : (
            <>
              <div className="listings-table-wrapper">
                <table className="listings-table">
                  <thead>
                    <tr>
                      <th>Business Name</th>
                      <th>Category</th>
                      <th>State</th>
                      <th>District</th>
                      <th>City</th>
                      <th>Address</th>
                      <th>Phone</th>
                      <th>Source</th>
                    </tr>
                  </thead>
                  <tbody>
                    {listings.length > 0 ? (
                      listings.map((item, index) => (
                        <tr key={`${item.business_name}-${item.city}-${index}`}>
                          <td className="business-name-cell">{item.business_name || "—"}</td>
                          <td>{item.category || "—"}</td>
                          <td>{item.state || "—"}</td>
                          <td>{item.district || "—"}</td>
                          <td>{item.city || "—"}</td>
                          <td className="address-cell" title={item.address || ""}>
                            {item.address || "—"}
                          </td>
                          <td>{item.phone || "—"}</td>
                          <td>{item.source || "—"}</td>
                        </tr>
                      ))
                    ) : (
                      <tr>
                        <td colSpan="8" className="listings-empty">
                          No business listings found for the selected filters.
                        </td>
                      </tr>
                    )}
                  </tbody>
                </table>
              </div>

              <div className="listings-pagination">
                <span>
                  Showing {listingsTotal === 0 ? 0 : (listingsPage - 1) * 25 + 1}
                  {"–"}
                  {Math.min(listingsPage * 25, listingsTotal)} of{" "}
                  {Number(listingsTotal).toLocaleString("en-IN")} records
                </span>
                <div>
                  <button
                    type="button"
                    className="refresh-btn"
                    disabled={listingsPage <= 1 || listingsLoading}
                    onClick={() => setListingsPage((page) => Math.max(1, page - 1))}
                  >
                    Previous
                  </button>
                  <span className="page-indicator">
                    Page {listingsPage} of {listingsPages}
                  </span>
                  <button
                    type="button"
                    className="refresh-btn"
                    disabled={listingsPage >= listingsPages || listingsLoading}
                    onClick={() => setListingsPage((page) => Math.min(listingsPages, page + 1))}
                  >
                    Next
                  </button>
                </div>
              </div>
            </>
          )}
        </section>

        {/* FOOTER */}
        <footer>
          Business Listings Analytics Dashboard · Powered by React, FastAPI & MySQL
        </footer>

      </main>

    </div>
  );
}

export default App;