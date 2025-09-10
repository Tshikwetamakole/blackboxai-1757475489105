export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-4">
            <h1 className="text-2xl font-bold text-gray-900">LimpopoConnect 2.0</h1>
            <nav className="space-x-4">
              <a href="/login" className="text-gray-600 hover:text-gray-900">Login</a>
              <a href="/register" className="bg-indigo-600 text-white px-4 py-2 rounded-md hover:bg-indigo-700">Register</a>
            </nav>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="text-center">
          <h2 className="text-4xl font-extrabold text-gray-900 sm:text-5xl">
            Connect in Limpopo
          </h2>
          <p className="mt-4 text-xl text-gray-600">
            Safe, secure dating and classifieds platform for meaningful connections.
          </p>
          <div className="mt-8">
            <a href="/ads" className="bg-indigo-600 text-white px-6 py-3 rounded-md text-lg hover:bg-indigo-700">
              Browse Ads
            </a>
          </div>
        </div>

        <div className="mt-16 grid grid-cols-1 md:grid-cols-3 gap-8">
          <div className="bg-white p-6 rounded-lg shadow-md">
            <h3 className="text-xl font-semibold text-gray-900">Dating</h3>
            <p className="mt-2 text-gray-600">Find meaningful relationships in your community.</p>
          </div>
          <div className="bg-white p-6 rounded-lg shadow-md">
            <h3 className="text-xl font-semibold text-gray-900">Classifieds</h3>
            <p className="mt-2 text-gray-600">Buy, sell, and trade with locals.</p>
          </div>
          <div className="bg-white p-6 rounded-lg shadow-md">
            <h3 className="text-xl font-semibold text-gray-900">Community</h3>
            <p className="mt-2 text-gray-600">Connect with people in Limpopo province.</p>
          </div>
        </div>
      </main>

      <footer className="bg-gray-800 text-white py-8">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <p>&copy; 2024 LimpopoConnect 2.0. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
}
