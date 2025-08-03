#include "therion.h"

int main(int /*argc*/, char** argv) {
    thexecute_cmd = argv[0];

    // This should not trigger the assert.
    thassert(true);
    // This should trigger the assert and exit the program.
    thassert(false);

    return 0;
}
