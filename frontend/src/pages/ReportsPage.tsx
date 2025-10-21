import { useState } from "react";
import { MainLayout } from "../components/layout";
import { Card } from "../components/common";
import {
  DollarSign,
  TrendingUp,
  FileText,
  Download,
  BarChart3,
  PieChart,
} from "lucide-react";
import { useAuth } from "../context/AuthContext";
import { toast } from "react-toastify";
import api from "../services/api";

interface ReportData {
  occupancy?: any[];
  revenue?: any[];
  serviceUsage?: any[];
  unpaidBalances?: any[];
}

const ReportsPage = () => {
  const { user } = useAuth();
  const [loading, setLoading] = useState(false);
  const [reportData, setReportData] = useState<ReportData>({});
  const [selectedReport, setSelectedReport] = useState<string>("occupancy");
  const [dateRange, setDateRange] = useState({
    startDate: new Date().toISOString().split("T")[0],
    endDate: new Date().toISOString().split("T")[0],
  });
  const [revenueParams, setRevenueParams] = useState({
    year: new Date().getFullYear(),
    month: new Date().getMonth() + 1,
  });

  const generateOccupancyReport = async () => {
    try {
      setLoading(true);
      const response = (await api.post("/reports/occupancy", {
        startDate: dateRange.startDate,
        endDate: dateRange.endDate,
        branchID: user?.branchID || 0,
      })) as any;

      setReportData((prev) => ({
        ...prev,
        occupancy: response.data?.report || [],
      }));
      toast.success("Occupancy report generated successfully");
    } catch (error: any) {
      console.error("Error generating occupancy report:", error);
      toast.error("Failed to generate occupancy report");
    } finally {
      setLoading(false);
    }
  };

  const generateRevenueReport = async () => {
    try {
      setLoading(true);
      const response = (await api.post("/reports/revenue", {
        year: revenueParams.year,
        month: revenueParams.month,
        branchID: user?.branchID || 0,
      })) as any;

      setReportData((prev) => ({
        ...prev,
        revenue: response.data?.report || [],
      }));
      toast.success("Revenue report generated successfully");
    } catch (error: any) {
      console.error("Error generating revenue report:", error);
      toast.error("Failed to generate revenue report");
    } finally {
      setLoading(false);
    }
  };

  const generateServiceUsageReport = async () => {
    try {
      setLoading(true);
      console.log("Generating service usage report with params:", {
        startDate: dateRange.startDate,
        endDate: dateRange.endDate,
        branchID: user?.branchID || 1,
      });

      const response = (await api.post("/reports/service-usage", {
        startDate: dateRange.startDate,
        endDate: dateRange.endDate,
        branchID: user?.branchID || 1,
      })) as any;

      console.log("Service usage response:", response);
      setReportData((prev) => ({
        ...prev,
        serviceUsage: response.data?.report || [],
      }));
      toast.success("Service usage report generated successfully");
    } catch (error: any) {
      console.error("Error generating service usage report:", error);
      toast.error("Failed to generate service usage report");
    } finally {
      setLoading(false);
    }
  };

  const getUnpaidBalances = async () => {
    try {
      setLoading(true);
      const branchId = user?.branchID || 1;
      console.log("Getting unpaid balances for branch:", branchId);

      const response = (await api.get(
        `/reports/unpaid-balances?branch_id=${branchId}`
      )) as any;

      console.log("Unpaid balances response:", response);
      setReportData((prev) => ({
        ...prev,
        unpaidBalances: response.data?.report || [],
      }));
      toast.success("Unpaid balances report generated successfully");
    } catch (error: any) {
      console.error("Error getting unpaid balances:", error);
      toast.error("Failed to load unpaid balances");
    } finally {
      setLoading(false);
    }
  };

  const exportReport = () => {
    const currentReportData = reportData[selectedReport as keyof ReportData];
    console.log("Export report - Current data:", currentReportData);
    console.log("Export report - Selected report:", selectedReport);
    console.log("Export report - All report data:", reportData);

    if (!currentReportData) {
      toast.error("No report data to export");
      return;
    }

    // Generate filename with timestamp
    const timestamp = new Date().toISOString().split("T")[0];
    const filename = `${selectedReport}-report-${timestamp}.json`;

    // Create downloadable content
    const reportContent = {
      reportType: selectedReport,
      generatedAt: new Date().toISOString(),
      parameters: selectedReport === "revenue" ? revenueParams : dateRange,
      data: currentReportData,
    };

    // Create and download file
    const dataStr = JSON.stringify(reportContent, null, 2);
    const dataBlob = new Blob([dataStr], { type: "application/json" });
    const url = URL.createObjectURL(dataBlob);

    const link = document.createElement("a");
    link.href = url;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);

    toast.success(`Report exported as ${filename}`);
  };

  const exportReportAsCSV = () => {
    const currentReportData = reportData[selectedReport as keyof ReportData];
    console.log("Export CSV - Current data:", currentReportData);
    console.log("Export CSV - Is array:", Array.isArray(currentReportData));
    console.log("Export CSV - Length:", currentReportData?.length);

    if (!currentReportData) {
      toast.error("No report data to export");
      return;
    }

    // Handle empty arrays or non-array data
    if (Array.isArray(currentReportData)) {
      if (currentReportData.length === 0) {
        toast.info("Report contains no data to export as CSV");
        return;
      }
    } else {
      // Convert single object to array for CSV export
      const arrayData = [currentReportData];
      const timestamp = new Date().toISOString().split("T")[0];
      const filename = `${selectedReport}-report-${timestamp}.csv`;

      const headers = Object.keys(arrayData[0]);
      const csvContent = [
        headers.join(","),
        ...arrayData.map((row) =>
          headers
            .map((header) => {
              const value = row[header];
              return typeof value === "string" &&
                (value as string).includes(",")
                ? `"${(value as string).replace(/"/g, '""')}"`
                : String(value);
            })
            .join(",")
        ),
      ].join("\n");

      const dataBlob = new Blob([csvContent], { type: "text/csv" });
      const url = URL.createObjectURL(dataBlob);
      const link = document.createElement("a");
      link.href = url;
      link.download = filename;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      URL.revokeObjectURL(url);

      toast.success(`Report exported as ${filename}`);
      return;
    }

    // Generate filename with timestamp
    const timestamp = new Date().toISOString().split("T")[0];
    const filename = `${selectedReport}-report-${timestamp}.csv`;

    // Convert to CSV
    const headers = Object.keys(currentReportData[0]);
    const csvContent = [
      headers.join(","),
      ...currentReportData.map((row) =>
        headers
          .map((header) => {
            const value = row[header];
            // Escape commas and quotes in values
            return typeof value === "string" && (value as string).includes(",")
              ? `"${(value as string).replace(/"/g, '""')}"`
              : String(value);
          })
          .join(",")
      ),
    ].join("\n");

    // Create and download file
    const dataBlob = new Blob([csvContent], { type: "text/csv" });
    const url = URL.createObjectURL(dataBlob);

    const link = document.createElement("a");
    link.href = url;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);

    toast.success(`Report exported as ${filename}`);
  };

  const reportTypes = [
    {
      id: "occupancy",
      title: "Room Occupancy",
      description: "View room occupancy rates and statistics",
      icon: <BarChart3 size={24} />,
      color: "bg-blue-50 border-blue-200",
      textColor: "text-blue-700",
      action: generateOccupancyReport,
    },
    {
      id: "revenue",
      title: "Revenue Report",
      description: "Monthly revenue and earnings analysis",
      icon: <DollarSign size={24} />,
      color: "bg-green-50 border-green-200",
      textColor: "text-green-700",
      action: generateRevenueReport,
    },
    {
      id: "service-usage",
      title: "Service Usage",
      description: "Track service utilization and popularity",
      icon: <PieChart size={24} />,
      color: "bg-purple-50 border-purple-200",
      textColor: "text-purple-700",
      action: generateServiceUsageReport,
    },
    {
      id: "unpaid-balances",
      title: "Unpaid Balances",
      description: "Outstanding payments and dues",
      icon: <FileText size={24} />,
      color: "bg-orange-50 border-orange-200",
      textColor: "text-orange-700",
      action: getUnpaidBalances,
    },
  ];

  return (
    <MainLayout>
      <div className="space-y-6">
        {/* Header */}
        <div>
          <h1 className="text-3xl font-bold text-gray-900">
            Reports & Analytics
          </h1>
          <p className="text-gray-600 mt-1">
            Generate and view comprehensive business reports
          </p>
        </div>

        {/* Report Type Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {reportTypes.map((report) => (
            <div
              key={report.id}
              className={`p-6 rounded-lg border cursor-pointer transition-all hover:shadow-lg ${
                selectedReport === report.id
                  ? `${report.color} ring-2 ring-opacity-50`
                  : "bg-white border-gray-200"
              }`}
              onClick={() => setSelectedReport(report.id)}
            >
              <div className="text-center space-y-4">
                <div
                  className={`mx-auto w-12 h-12 rounded-full flex items-center justify-center ${
                    selectedReport === report.id ? report.color : "bg-gray-50"
                  }`}
                >
                  <span
                    className={
                      selectedReport === report.id
                        ? report.textColor
                        : "text-gray-600"
                    }
                  >
                    {report.icon}
                  </span>
                </div>
                <div>
                  <h3 className="text-lg font-semibold text-gray-900">
                    {report.title}
                  </h3>
                  <p className="text-sm text-gray-600 mt-1">
                    {report.description}
                  </p>
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Report Parameters and Generation */}
        <Card title="Generate Report">
          <div className="space-y-6">
            {/* Date Range Parameters (for occupancy and service usage) */}
            {(selectedReport === "occupancy" ||
              selectedReport === "service-usage") && (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Start Date
                  </label>
                  <input
                    type="date"
                    value={dateRange.startDate}
                    onChange={(e) =>
                      setDateRange((prev) => ({
                        ...prev,
                        startDate: e.target.value,
                      }))
                    }
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    End Date
                  </label>
                  <input
                    type="date"
                    value={dateRange.endDate}
                    onChange={(e) =>
                      setDateRange((prev) => ({
                        ...prev,
                        endDate: e.target.value,
                      }))
                    }
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                </div>
              </div>
            )}

            {/* Revenue Parameters */}
            {selectedReport === "revenue" && (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Year
                  </label>
                  <input
                    type="number"
                    min="2020"
                    max="2030"
                    value={revenueParams.year}
                    onChange={(e) =>
                      setRevenueParams((prev) => ({
                        ...prev,
                        year: parseInt(e.target.value),
                      }))
                    }
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Month
                  </label>
                  <select
                    value={revenueParams.month}
                    onChange={(e) =>
                      setRevenueParams((prev) => ({
                        ...prev,
                        month: parseInt(e.target.value),
                      }))
                    }
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  >
                    {Array.from({ length: 12 }, (_, i) => (
                      <option key={i + 1} value={i + 1}>
                        {new Date(2023, i).toLocaleString("default", {
                          month: "long",
                        })}
                      </option>
                    ))}
                  </select>
                </div>
              </div>
            )}

            {/* Generate Button */}
            <div className="flex justify-between items-center">
              <button
                onClick={
                  reportTypes.find((r) => r.id === selectedReport)?.action
                }
                disabled={loading}
                className="btn-primary flex items-center gap-2"
              >
                <TrendingUp size={15} />
                {loading ? "Generating..." : "Generate Report"}
              </button>

              {/* Show export buttons when report data exists */}
              {reportData[selectedReport as keyof ReportData] &&
                (Array.isArray(reportData[selectedReport as keyof ReportData])
                  ? reportData[selectedReport as keyof ReportData]!.length > 0
                  : reportData[selectedReport as keyof ReportData]) && (
                  <div className="flex gap-2">
                    <button
                      onClick={exportReport}
                      className="btn-primary flex items-center gap-2"
                    >
                      <Download size={15} />
                      Export JSON
                    </button>
                    <button
                      onClick={exportReportAsCSV}
                      className="btn-primary flex items-center gap-2"
                    >
                      <FileText size={15} />
                      Export CSV
                    </button>
                  </div>
                )}
            </div>
          </div>
        </Card>

        {/* Report Results */}
        {reportData[selectedReport as keyof ReportData] && (
          <Card title="Report Results">
            <div className="space-y-4">
              {/* Table view for better readability */}
              {Array.isArray(reportData[selectedReport as keyof ReportData]) &&
              reportData[selectedReport as keyof ReportData]!.length > 0 ? (
                <div className="overflow-x-auto">
                  <table className="min-w-full bg-white border border-gray-200 rounded-lg">
                    <thead className="bg-gray-50">
                      <tr>
                        {Object.keys(
                          reportData[selectedReport as keyof ReportData]![0]
                        ).map((header) => (
                          <th
                            key={header}
                            className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider border-b"
                          >
                            {header
                              .replace(/([A-Z])/g, " $1")
                              .replace(/^./, (str) => str.toUpperCase())}
                          </th>
                        ))}
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-gray-200">
                      {reportData[selectedReport as keyof ReportData]!.map(
                        (row: any, index: number) => (
                          <tr key={index} className="hover:bg-gray-50">
                            {Object.entries(row).map(([key, value]) => (
                              <td
                                key={key}
                                className="px-6 py-4 whitespace-nowrap text-sm text-gray-900"
                              >
                                {typeof value === "number" &&
                                key.toLowerCase().includes("rate")
                                  ? `${value}%`
                                  : typeof value === "number" &&
                                    key.toLowerCase().includes("revenue")
                                  ? `$${value.toLocaleString()}`
                                  : String(value)}
                              </td>
                            ))}
                          </tr>
                        )
                      )}
                    </tbody>
                  </table>
                </div>
              ) : (
                <div className="bg-gray-50 p-4 rounded-lg">
                  <pre className="text-sm text-gray-700 whitespace-pre-wrap">
                    {JSON.stringify(
                      reportData[selectedReport as keyof ReportData],
                      null,
                      2
                    )}
                  </pre>
                </div>
              )}

              {/* Summary Statistics */}
              {selectedReport === "occupancy" &&
                Array.isArray(reportData.occupancy) &&
                reportData.occupancy.length > 0 && (
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-6">
                    <div className="bg-blue-50 p-4 rounded-lg">
                      <p className="text-sm text-blue-700 font-medium">
                        Average Occupancy
                      </p>
                      <p className="text-2xl font-bold text-blue-900">
                        {(
                          reportData.occupancy.reduce(
                            (sum: number, item: any) =>
                              sum + (item.occupancyRate || 0),
                            0
                          ) / reportData.occupancy.length
                        ).toFixed(1)}
                        %
                      </p>
                    </div>
                    <div className="bg-green-50 p-4 rounded-lg">
                      <p className="text-sm text-green-700 font-medium">
                        Total Rooms
                      </p>
                      <p className="text-2xl font-bold text-green-900">
                        {reportData.occupancy.reduce(
                          (sum: number, item: any) =>
                            sum + (item.totalRooms || 0),
                          0
                        )}
                      </p>
                    </div>
                    <div className="bg-purple-50 p-4 rounded-lg">
                      <p className="text-sm text-purple-700 font-medium">
                        Occupied Rooms
                      </p>
                      <p className="text-2xl font-bold text-purple-900">
                        {reportData.occupancy.reduce(
                          (sum: number, item: any) =>
                            sum + (item.occupiedRooms || 0),
                          0
                        )}
                      </p>
                    </div>
                  </div>
                )}

              {selectedReport === "revenue" &&
                Array.isArray(reportData.revenue) &&
                reportData.revenue.length > 0 && (
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-6">
                    <div className="bg-green-50 p-4 rounded-lg">
                      <p className="text-sm text-green-700 font-medium">
                        Total Revenue
                      </p>
                      <p className="text-2xl font-bold text-green-900">
                        $
                        {reportData.revenue
                          .reduce(
                            (sum: number, item: any) =>
                              sum + (item.totalRevenue || 0),
                            0
                          )
                          .toLocaleString()}
                      </p>
                    </div>
                    <div className="bg-blue-50 p-4 rounded-lg">
                      <p className="text-sm text-blue-700 font-medium">
                        Room Revenue
                      </p>
                      <p className="text-2xl font-bold text-blue-900">
                        $
                        {reportData.revenue
                          .reduce(
                            (sum: number, item: any) =>
                              sum + (item.roomRevenue || 0),
                            0
                          )
                          .toLocaleString()}
                      </p>
                    </div>
                    <div className="bg-purple-50 p-4 rounded-lg">
                      <p className="text-sm text-purple-700 font-medium">
                        Total Bookings
                      </p>
                      <p className="text-2xl font-bold text-purple-900">
                        {reportData.revenue.reduce(
                          (sum: number, item: any) =>
                            sum + (item.totalBookings || 0),
                          0
                        )}
                      </p>
                    </div>
                  </div>
                )}
            </div>
          </Card>
        )}

        {/* Quick Stats */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <Card className="bg-gradient-to-r from-blue-50 to-blue-100 border-blue-200">
            <div className="flex items-center gap-4">
              <div className="w-12 h-12 bg-blue-200 rounded-full flex items-center justify-center">
                <BarChart3 className="text-blue-700" size={24} />
              </div>
              <div>
                <p className="text-sm text-blue-700 font-medium">
                  Total Reports
                </p>
                <p className="text-2xl font-bold text-blue-900">
                  {Object.keys(reportData).length}
                </p>
              </div>
            </div>
          </Card>

          <Card className="bg-gradient-to-r from-green-50 to-green-100 border-green-200">
            <div className="flex items-center gap-4">
              <div className="w-12 h-12 bg-green-200 rounded-full flex items-center justify-center">
                <DollarSign className="text-green-700" size={24} />
              </div>
              <div>
                <p className="text-sm text-green-700 font-medium">
                  Reports Generated
                </p>
                <p className="text-2xl font-bold text-green-900">Today</p>
              </div>
            </div>
          </Card>

          <Card className="bg-gradient-to-r from-purple-50 to-purple-100 border-purple-200">
            <div className="flex items-center gap-4">
              <div className="w-12 h-12 bg-purple-200 rounded-full flex items-center justify-center">
                <FileText className="text-purple-700" size={24} />
              </div>
              <div>
                <p className="text-sm text-purple-700 font-medium">
                  Last Generated
                </p>
                <p className="text-2xl font-bold text-purple-900">
                  {new Date().toLocaleDateString()}
                </p>
              </div>
            </div>
          </Card>
        </div>
      </div>
    </MainLayout>
  );
};

export default ReportsPage;
