export default function GalleryPage() {
  return (
    <div className="max-w-6xl mx-auto space-y-8">
      <h2 className="text-3xl font-bold text-center">Галерея коміксів</h2>
      
      <div className="bg-white p-12 rounded-xl shadow-md text-center">
        <p className="text-xl text-gray-600 mb-4">
          Галерея порожня
        </p>
        <p className="text-gray-500">
          Створіть свій перший комікс у генераторі!
        </p>
        <a
          href="/generator"
          className="inline-block mt-6 bg-joj-blue text-white px-6 py-3 rounded-lg font-semibold hover:bg-joj-blue/80"
        >
          Перейти до генератора
        </a>
      </div>

      {/* Приклад структури для майбутніх коміксів */}
      <div className="grid md:grid-cols-3 gap-6 opacity-50">
        {[1, 2, 3].map((i) => (
          <div
            key={i}
            className="bg-gray-100 p-4 rounded-xl border-2 border-dashed border-gray-300"
          >
            <div className="aspect-square bg-gray-200 rounded-lg mb-4" />
            <h3 className="font-bold text-gray-400">Комікс #{i}</h3>
            <p className="text-sm text-gray-400">Від Рекрута до Солдата</p>
          </div>
        ))}
      </div>
    </div>
  );
}
