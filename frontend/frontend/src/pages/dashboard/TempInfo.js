import React from "react";
import Header from "../../components/Header";
import Footer from "../../components/Footer";
import Sidebar from "../../components/Sidebar";
import ChartComponent from "../../components/ChartComponent";

const tempData = [
  { time: "00:00", value: 22 },
  { time: "06:00", value: 24 },
  { time: "12:00", value: 28 },
  { time: "18:00", value: 26 },
  { time: "23:59", value: 22 },
];

const DashboardTempPage = () => {
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
            <div className="w-[60%]">
              <h2 className="text-xl font-bold mb-4">Nhiệt độ hiện tại</h2>
              <div className="w-48 p-4 bg-white border shadow rounded-lg flex items-center">
                <span className="text-2xl mr-2">🌡️</span>
                <div>
                  <p className="text-gray-700">Nhiệt độ</p>
                  <p className="font-bold">25&deg;C</p>
                </div>
              </div>
            </div>
            <div className="w-[40%] pr-6">
              <h2 className="text-xl font-bold mb-4">Mức độ sáng cần thiết</h2>
              <div className="">
                <div className="grid grid-rows-2 gap-y-2 p-4 bg-white border shadow rounded-lg items-center font-bold">
                  <div className="flex justify-between">
                    <div className="w-[18%]">
                      <p>Từ</p>
                    </div>
                    <div className="flex-grow mx-1 bg-gray-300 rounded-sm px-8">
                      <p className="text-center">20&deg;C</p>
                    </div>
                    <div className="w-[26%]"></div>
                  </div>
                  <div className="flex justify-between">
                    <div className="w-[18%]">
                      <p>Đến</p>
                    </div>
                    <div className="flex-grow mx-1 bg-gray-300 rounded-sm px-8">
                      <p className="text-center">30&deg;C</p>
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
          <div className="grid grid-cols-2 gap-x-2 w-[50%] font-bold">
            <div className="p-4 py-6 bg-white border shadow rounded-lg flex items-center">
              <input type="radio" name="light-mode" className="mr-2"></input>
              <p>Thủ công</p>
            </div>
            <div className="p-4 py-6 bg-white border shadow rounded-lg flex items-center">
              <input type="radio" name="light-mode" className="mr-2"></input>
              <p>Tự động</p>
            </div>
          </div>

          {/* Thống kê biểu đồ */}
          <div className="flex">
            <div className="w-[60%]">
              <h2 className="text-xl font-bold mt-6">Điều chỉnh đèn sưởi</h2>
              <div className="w-48 bg-white border shadow rounded-lg flex items-center p-4 py-6">
                <label class="inline-flex items-center cursor-pointer">
                  <input type="checkbox" value="" class="sr-only peer"></input>
                  <div class="relative w-11 h-6 bg-gray-400 peer-focus:outline-none peer-focus:ring-1 peer-focus:ring-gray-800 rounded-full peer  peer-checked:after:translate-x-full rtl:peer-checked:after:-translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:start-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all  peer-checked:bg-green-500 dark:peer-checked:bg-green-500"></div>
                  <span class="ms-3 text-sm font-bold">Bật</span>
                </label>
              </div>
            </div>
            <div className="w-[40%]">
              <h2 className="text-xl font-bold mt-6">
                Điều chỉnh quạt thông gió
              </h2>
              <div className="w-48 bg-white border shadow rounded-lg flex items-center p-4 py-6">
                <label class="inline-flex items-center cursor-pointer">
                  <input type="checkbox" value="" class="sr-only peer"></input>
                  <div class="relative w-11 h-6 bg-gray-400 peer-focus:outline-none peer-focus:ring-1 peer-focus:ring-gray-800 rounded-full peer  peer-checked:after:translate-x-full rtl:peer-checked:after:-translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:start-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all  peer-checked:bg-green-500 dark:peer-checked:bg-green-500"></div>
                  <span class="ms-3 text-sm font-bold">Bật</span>
                </label>
              </div>
            </div>
          </div>

          {/* Biểu đồ ánh sáng */}
          <h2 className="text-xl font-bold mt-6 mb-2">Lịch sử nhiệt độ</h2>
          <div className="w-[60%] border shadow rounded-lg">
            <ChartComponent title="" data={tempData} color="#fdd835" />
          </div>
        </div>
      </div>
      {/* Footer */}
      <Footer />
    </div>
  );
};

export default DashboardTempPage;
