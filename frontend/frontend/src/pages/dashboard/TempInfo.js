import React from "react";
import Header from "../../components/Header";
import Footer from "../../components/Footer";
import Sidebar from "../../components/Sidebar";

const heatHistoryData = [
  { time: "14:00", status: "Bật" },
  { time: "13:00", status: "Tắt" },
  { time: "12:00", status: "Bật" },
  { time: "11:00", status: "Tắt" },
];

const fanHistoryData = [
  { time: "14:00", status: "Bật" },
  { time: "13:00", status: "Tắt" },
  { time: "12:00", status: "Bật" },
  { time: "10:00", status: "Tắt" },
];


const DashboardTempPage = () => {
  return (
    <div className="flex flex-col min-h-screen">
      <Header />
      {/* Nội dung chính */}
      <div className="flex flex-grow">
        {/* Sidebar */}
        <Sidebar activeItem="temperature" />

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
                    <button className="bg-[#598868] text-white text-xs hover:bg-green-600 rounded-md px-2">
                      Chỉnh sửa
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Chế độ điều chỉnh */}
          <h2 className="text-xl font-bold mt-6">Chế độ điều chỉnh</h2>
          <div className="grid grid-cols-2 gap-x-2 w-[50%] font-bold">
            <div className="p-4 py-6 bg-white border shadow rounded-lg flex items-center">
              <input type="radio" name="light-mode" className="mr-2" />
              <p>Thủ công</p>
            </div>
            <div className="p-4 py-6 bg-white border shadow rounded-lg flex items-center">
              <input type="radio" name="light-mode" className="mr-2" />
              <p>Tự động</p>
            </div>
          </div>

          {/* Điều chỉnh đèn và quạt */}
          <div className="flex justify-between mt-6">
            <div className="w-[48%]">
              <h2 className="text-xl font-bold mb-2">Điều chỉnh đèn sưởi</h2>
              <div className="bg-white border shadow rounded-lg flex items-center p-4 py-6">
                <label className="inline-flex items-center cursor-pointer">
                  <input type="checkbox" className="sr-only peer" />
                  <div className="relative w-11 h-6 bg-gray-400 peer-focus:outline-none peer-focus:ring-1 peer-focus:ring-gray-800 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:start-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-green-500"></div>
                  <span className="ms-3 text-sm font-bold">Bật</span>
                </label>
              </div>
            </div>

            <div className="w-[48%]">
              <h2 className="text-xl font-bold mb-2">Điều chỉnh quạt thông gió</h2>
              <div className="bg-white border shadow rounded-lg flex items-center p-4 py-6">
                <label className="inline-flex items-center cursor-pointer">
                  <input type="checkbox" className="sr-only peer" />
                  <div className="relative w-11 h-6 bg-gray-400 peer-focus:outline-none peer-focus:ring-1 peer-focus:ring-gray-800 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:start-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-green-500"></div>
                  <span className="ms-3 text-sm font-bold">Bật</span>
                </label>
              </div>
            </div>
          </div>

          {/* Lịch sử hoạt động */}
          <div className="flex justify-between mt-6">
            <div className="w-[48%]">
              <h2 className="text-xl font-bold mb-2">Lịch sử hoạt động đèn sưởi</h2>
              <div className="border rounded-lg shadow-md bg-white">
                {heatHistoryData.map((item, index) => (
                  <div
                    key={index}
                    className="flex items-center px-4 py-3 border-b last:border-none"
                  >
                    <span className="mr-2 pl-2">🕒</span>
                    <span className="text-gray-500 text-sm w-[20%]">{item.time}</span>
                    <span
                      className={`ml-auto font-semibold ${
                        item.status === "Bật" ? "text-green-600" : "text-red-600"
                      }`}
                    >
                      {item.status}
                    </span>
                  </div>
                ))}
              </div>
            </div>
            <div className="w-[48%]">
              <h2 className="text-xl font-bold mb-2">Lịch sử hoạt động quạt thông gió</h2>
              <div className="border rounded-lg shadow-md bg-white">
                {fanHistoryData.map((item, index) => (
                  <div
                    key={index}
                    className="flex items-center px-4 py-3 border-b last:border-none"
                  >
                    <span className="mr-2 pl-2">🕒</span>
                    <span className="text-gray-500 text-sm w-[20%]">{item.time}</span>
                    <span
                      className={`ml-auto font-semibold ${
                        item.status === "Bật" ? "text-green-600" : "text-red-600"
                      }`}
                    >
                      {item.status}
                    </span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
      <Footer />
    </div>
  );
};

export default DashboardTempPage;
