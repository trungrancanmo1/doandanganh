import React, { useState } from "react";

const AccountSettings = () => {
  const [profileImage, setProfileImage] = useState("/default-avatar.png");
  const [fullName, setFullName] = useState("Nguyễn Văn A");
  const email = "nguyenvana@example.com";
  const [phone, setPhone] = useState("0123456789");
  const [currentPassword, setCurrentPassword] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");

  const handleImageChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setProfileImage(URL.createObjectURL(file));
    }
  };

  const handleSaveChanges = () => {
    alert("Thông tin cá nhân đã được cập nhật!");
  };

  const handleChangePassword = () => {
    if (newPassword !== confirmPassword) {
      alert("Mật khẩu xác nhận không khớp!");
      return;
    }
    alert("Mật khẩu đã được thay đổi thành công!");
  };

  return (
    <div className="max-w-2xl mx-auto p-6 bg-white shadow-lg rounded-lg mt-6">
      <h2 className="text-2xl font-bold mb-4">Cài Đặt Tài Khoản</h2>

      {/* Thông Tin Cá Nhân */}
      <div className="mb-6">
        <h3 className="text-lg font-semibold mb-2">Thông Tin Cá Nhân</h3>
        <div className="flex items-center space-x-4 mb-4">
          <img src={profileImage} alt="Avatar" className="w-20 h-20 rounded-full border" />
          <input type="file" accept="image/*" onChange={handleImageChange} />
        </div>
        <label className="block mb-1">Họ và tên</label>
        <input type="text" value={fullName} onChange={(e) => setFullName(e.target.value)} className="w-full p-2 border rounded mb-3" />
        <label className="block mb-1">Email</label>
        <input type="email" value={email} disabled className="w-full p-2 border bg-gray-100 rounded mb-3" />
        <label className="block mb-1">Số điện thoại</label>
        <input type="text" value={phone} onChange={(e) => setPhone(e.target.value)} className="w-full p-2 border rounded mb-3" />
        <button onClick={handleSaveChanges} className="px-4 py-2 bg-green-500 text-white rounded-lg">Lưu thay đổi</button>
      </div>

      {/* Thay Đổi Mật Khẩu */}
      <div>
        <h3 className="text-lg font-semibold mb-2">Thay Đổi Mật Khẩu</h3>
        <label className="block mb-1">Mật khẩu hiện tại</label>
        <input type="password" value={currentPassword} onChange={(e) => setCurrentPassword(e.target.value)} className="w-full p-2 border rounded mb-3" />
        <label className="block mb-1">Mật khẩu mới</label>
        <input type="password" value={newPassword} onChange={(e) => setNewPassword(e.target.value)} className="w-full p-2 border rounded mb-3" />
        <label className="block mb-1">Xác nhận mật khẩu mới</label>
        <input type="password" value={confirmPassword} onChange={(e) => setConfirmPassword(e.target.value)} className="w-full p-2 border rounded mb-3" />
        <button onClick={handleChangePassword} className="px-4 py-2 bg-blue-500 text-white rounded-lg">Đổi mật khẩu</button>
      </div>
    </div>
  );
};

export default AccountSettings;
