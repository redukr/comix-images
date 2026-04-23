import Link from "next/link";
import { BookOpen, Sparkles, Image } from "lucide-react";

export default function HomePage() {
  return (
    <div className="space-y-12">
      {/* Hero Section */}
      <section className="text-center py-12 bg-gradient-to-r from-joj-blue to-joj-yellow rounded-2xl">
        <h2 className="text-4xl font-bold text-white mb-4 drop-shadow-lg">
          Від Рекрута до Генерала
        </h2>
        <p className="text-xl text-white/90 max-w-2xl mx-auto">
          Генератор коміксів про кар'єрний ріст в ЗСУ на основі гри JOJ.
          Створюйте унікальні історії з AI та власними ігровими картами.
        </p>
        <div className="mt-8 flex gap-4 justify-center">
          <Link
            href="/generator"
            className="bg-white text-joj-blue px-6 py-3 rounded-lg font-semibold hover:bg-gray-100 transition"
          >
            Створити комікс
          </Link>
          <Link
            href="/gallery"
            className="bg-joj-blue text-white border-2 border-white px-6 py-3 rounded-lg font-semibold hover:bg-joj-blue/80 transition"
          >
            Переглянути приклади
          </Link>
        </div>
      </section>

      {/* Features */}
      <section className="grid md:grid-cols-3 gap-8">
        <div className="bg-white p-6 rounded-xl shadow-md border border-gray-200">
          <Sparkles className="w-12 h-12 text-joj-yellow mb-4" />
          <h3 className="text-xl font-bold mb-2">AI Генерація</h3>
          <p className="text-gray-600">
            Використовуйте локальний LLM для генерації сюжетів та діалогів.
            Інтеграція з LM Studio.
          </p>
        </div>
        
        <div className="bg-white p-6 rounded-xl shadow-md border border-gray-200">
          <Image className="w-12 h-12 text-military-green mb-4" />
          <h3 className="text-xl font-bold mb-2">ComfyUI</h3>
          <p className="text-gray-600">
            Генерація та обробка зображень через локальний ComfyUI.
            Повний контроль над стилем.
          </p>
        </div>
        
        <div className="bg-white p-6 rounded-xl shadow-md border border-gray-200">
          <BookOpen className="w-12 h-12 text-joj-blue mb-4" />
          <h3 className="text-xl font-bold mb-2">JOJ Інтеграція</h3>
          <p className="text-gray-600">
            Використовуйте ігрові карти, ранги та всесвіт JOJ.
            Більше 200 унікальних зображень.
          </p>
        </div>
      </section>

      {/* How it works */}
      <section className="bg-white p-8 rounded-2xl shadow-lg">
        <h3 className="text-2xl font-bold mb-6 text-center">Як це працює</h3>
        <div className="grid md:grid-cols-4 gap-4 text-center">
          <div className="space-y-2">
            <div className="w-12 h-12 bg-joj-blue text-white rounded-full flex items-center justify-center mx-auto font-bold text-xl">
              1
            </div>
            <p className="font-semibold">Оберіть ранги</p>
            <p className="text-sm text-gray-600">Від рекрута до генерала</p>
          </div>
          <div className="space-y-2">
            <div className="w-12 h-12 bg-joj-blue text-white rounded-full flex items-center justify-center mx-auto font-bold text-xl">
              2
            </div>
            <p className="font-semibold">AI генерує сюжет</p>
            <p className="text-sm text-gray-600">Через LLM Studio</p>
          </div>
          <div className="space-y-2">
            <div className="w-12 h-12 bg-joj-blue text-white rounded-full flex items-center justify-center mx-auto font-bold text-xl">
              3
            </div>
            <p className="font-semibold">Створення зображень</p>
            <p className="text-sm text-gray-600">ComfyUI або JOJ карти</p>
          </div>
          <div className="space-y-2">
            <div className="w-12 h-12 bg-joj-blue text-white rounded-full flex items-center justify-center mx-auto font-bold text-xl">
              4
            </div>
            <p className="font-semibold">Компонування</p>
            <p className="text-sm text-gray-600">PDF або HTML експорт</p>
          </div>
        </div>
      </section>
    </div>
  );
}
