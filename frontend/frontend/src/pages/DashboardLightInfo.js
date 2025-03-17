import React from "react";
import Header from "../components/Header";
import Footer from "../components/Footer";
import Sidebar from "../components/Sidebar";
import DashboardCharts from "../components/DashboardCharts";


const DashboardLightPage = () => {
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
          <div className="flex justify-between">
            <div className="w-[30%]">
              <h2 className="text-xl font-bold mb-4">Độ sáng hiện tại</h2>
              <div className="p-4 bg-white shadow rounded-lg flex items-center">
                <span className="text-2xl mr-2">☀️</span>
                <div>
                  <p className="text-gray-700">Ánh sáng</p>
                  <p className="font-bold">60000 lux</p>
                </div>
              </div>
            </div>
            <div className="w-[40%]">
              <h2 className="text-xl font-bold mb-4">Mức độ sáng cần thiết</h2>
              <div className="">
                <div className="grid grid-rows-2 gap-y-2 p-4 bg-white shadow rounded-lg items-center font-bold">
                  <div className="flex justify-between">
                    <div className="w-[18%]">
                      <p>Từ</p>
                    </div>
                    <div className="flex-grow mx-1 bg-gray-300">
                      <p className="text-center">70000 lux</p>
                    </div>
                    <div className="w-[26%]"></div>
                  </div>
                  <div className="flex justify-between">
                    <div className="w-[18%]">
                      <p>Đến</p>
                    </div>
                    <div className="flex-grow mx-1 bg-gray-300">
                      <p className="text-center">80000 lux</p>
                    </div>
                    <div className="w-[26%] flex justify-end">
                      <button
                        href="#"
                        className="bg-[#598868] text-white text-xs hover:bg-green-600 rounded-md px-2"
                      >
                        Chỉnh sửa
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Hình ảnh cây */}
          <h2 className="text-xl font-bold mt-6">Chế độ điều chỉnh</h2>
          <div className="grid grid-cols-2 gap-x-2 w-[50%]">
            <div className="p-4 bg-white shadow rounded-lg flex items-center">
              <span className="text-2xl mr-2">☀️</span>
              <div>
                <p className="text-gray-700">Ánh sáng</p>
                <p className="font-bold">60000 lux</p>
              </div>
            </div>
            <div className="p-4 bg-white shadow rounded-lg flex items-center">
              <span className="text-2xl mr-2">☀️</span>
              <div>
                <p className="text-gray-700">Ánh sáng</p>
                <p className="font-bold">60000 lux</p>
              </div>
            </div>
          </div>

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

export default DashboardLightPage;
