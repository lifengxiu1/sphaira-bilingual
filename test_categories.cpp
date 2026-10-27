#include "app_category.hpp"
#include <cassert>

using namespace sphaira::category;

int main() {
    assert(ForPackage("jksv", "tool") == GameTools);
    assert(ForPackage("FPSLocker", "tool") == GameTools);
    assert(ForPackage("OpenTTD", "game") == Games);
    assert(ForPackage("mGBA", "emu") == Emulators);
    assert(ForPackage("Moonlight-Switch", "tool") == MediaNetwork);
    assert(ForPackage("Calculator_NX", "tool") == Other);
    assert(ForPath("/switch/TranslateNX.nro") == GameTools);
    assert(ForPath("sdmc:/switch/haze.nro") == SystemTools);
    assert(ForPath("/switch/unknown.nro") == Other);
    assert(ForPackage("future-game", "game") == Games);
    assert(ForPackage("future-emulator", "emu") == Emulators);
    assert(ForPackage("future-tool", "tool") == SystemTools);
    assert(ForPackage("future-unknown", "unknown") == Other);
    assert(NormalizeFilter(4) == SystemTools);
    assert(NormalizeFilter(5) == SystemTools);
    assert(NormalizeFilter(6) == Other);
    assert(NormalizeFilter(-1) == All);
    assert(NormalizeFilter(10) == All);
    for (const auto type : Filters) {
        assert(Filters[FilterIndex(type)] == type);
        assert(Matches(All, type));
        assert(Matches(type, type));
    }
    assert(!Matches(GameTools, Games));
}
