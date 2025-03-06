import { readFileSync } from "fs";
import { hello } from "../myTools";

describe("Hello", () => {
    test("Filter Alpha Regression Playwright runs", () => {
        const CONFIG = {
            START: "2025-03-01",
            END: "2025-03-06",
            NAMES: ["Alpha Regression Playwright 0 07 * * *", "Alpha Regression Playwright 0 13 * * *"]
        }

        const workflows = JSON.parse(readFileSync("/Users/billcarlo.vergara/Projects/personal_tools/input/workflowRuns.json", "utf-8"))
        const filtered = workflows
            .filter((obj) => obj.createdAt >= CONFIG.START && obj.createdAt < CONFIG.END)
            .filter(obj => CONFIG.NAMES.includes(obj.name))

        console.log(
            '~/Projects/personal_tools/myNodeScripts/src/__tests__/myTools.test.js:8',
            'billy',
            filtered
        )
    })
})