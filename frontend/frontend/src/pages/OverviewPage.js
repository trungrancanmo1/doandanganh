import React from "react";
import Header from "../components/Header";
import Footer from "../components/Footer";
import Sidebar from "../components/Sidebar";
import DashboardCharts from "../components/DashboardCharts";
import PlantPicture from "../assets/plantPicture.jpg";

const DashboardOverview = () => {
  return (
    <div className="flex flex-col min-h-screen">
      {" "}
      {/* Đổi h-screen thành min-h-screen */}
      <Header />
      {/* Nội dung chính */}
      <div className="flex flex-grow">
        {" "}
        {/* Thêm flex-grow để chiếm toàn bộ không gian */}
        {/* Sidebar */}
        <Sidebar />
        {/* Nội dung dashboard */}
        <div className="flex-1 p-6">
          <h2 className="text-xl font-bold mb-4">
            Điều kiện môi trường hiện tại
          </h2>
          <div className="grid grid-cols-3 gap-6">
            <div className="p-4 bg-white shadow rounded-lg flex items-center">
              <span className="text-2xl mr-2">🌡️</span>
              <div>
                <p className="text-gray-700">Nhiệt độ</p>
                <p className="font-bold">25°C</p>
              </div>
            </div>
            <div className="p-4 bg-white shadow rounded-lg flex items-center">
              <span className="text-2xl mr-2">☀️</span>
              <div>
                <p className="text-gray-700">Ánh sáng</p>
                <p className="font-bold">60000 lux</p>
              </div>
            </div>
            <div className="p-4 bg-white shadow rounded-lg flex items-center">
              <span className="text-2xl mr-2">💧</span>
              <div>
                <p className="text-gray-700">Độ ẩm</p>
                <p className="font-bold">60%</p>
              </div>
            </div>
          </div>

          {/* Hình ảnh cây */}
          <h2 className="text-xl font-bold mt-6">Ảnh chụp cây gần đây nhất</h2>
          <img
            src={PlantPicture}
            alt="Cây xanh"
            className="w-60 h-40 mt-2 rounded shadow"
          />

          {/* Thống kê biểu đồ */}
          <h2 className="text-xl font-bold mt-6">Thống kê trong 24 giờ qua</h2>
          <DashboardCharts />
        </div>
      </div>
      {/* Footer */}
      <Footer />
    </div>
  );
};

export default DashboardOverview;
