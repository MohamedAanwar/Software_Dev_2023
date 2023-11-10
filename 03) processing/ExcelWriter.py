import os
import pandas as pd
from CustomTime import Time
import threading
from Thread_basics.cls_Readucer import Readucer
import concurrent.futures


class ExcelWriter(threading.Thread, Readucer):
    def __init__(self, excelQueue, sheetPath):
        super().__init__()
        self.excelQueue = excelQueue
        self.sheetPath = sheetPath
        self.DictTotalTIme = {}

    def TotalTimeCalc(self, listChange, sheetPath):
        try:
            head_motion_center = [
                d["head movement time span"]
                for d in listChange
                if "head status" in d and d["head status"] == "center"
            ]
            head_motion_left = [
                d["head movement time span"]
                for d in listChange
                if "head status" in d and d["head status"] == "left"
            ]
            head_motion_right = [
                d["head movement time span"]
                for d in listChange
                if "head status" in d and d["head status"] == "right"
            ]
            head_motion_none = [
                d["head movement time span"]
                for d in listChange
                if "head status" in d and d["head status"] == "none"
            ]

            wing_motion_on = [
                d["wing movement time span"]
                for d in listChange
                if "wing status" in d and d["wing status"] == "on"
            ]
            wing_motion_off = [
                d["wing movement time span"]
                for d in listChange
                if "wing status" in d and d["wing status"] == "off"
            ]
            wing_motion_none = [
                d["wing movement time span"]
                for d in listChange
                if "wing status" in d and d["wing status"] == "none"
            ]

            leg_motion_up = [
                d["leg movement time span"]
                for d in listChange
                if "leg status" in d and d["leg status"] == "up"
            ]
            leg_motion_down = [
                d["leg movement time span"]
                for d in listChange
                if "leg status" in d and d["leg status"] == "down"
            ]
            leg_motion_none = [
                d["leg movement time span"]
                for d in listChange
                if "leg status" in d and d["leg status"] == "none"
            ]

            tail_motion_center = [
                d["tail movement time span"]
                for d in listChange
                if "tail status" in d and d["tail status"] == "center"
            ]
            tail_motion_left = [
                d["tail movement time span"]
                for d in listChange
                if "tail status" in d and d["tail status"] == "left"
            ]
            tail_motion_right = [
                d["tail movement time span"]
                for d in listChange
                if "tail status" in d and d["tail status"] == "right"
            ]
            tail_motion_none = [
                d["tail movement time span"]
                for d in listChange
                if "tail status" in d and d["tail status"] == "none"
            ]

            head_center = 0
            head_left = 0
            head_right = 0
            head_none = 0
            head_total = 0
            for i in head_motion_center:
                head_center += Time.reverseFormulateTime(i)
            head_total += head_center
            head_center = Time.formulateTime(head_center)

            for i in head_motion_left:
                head_left += Time.reverseFormulateTime(i)
            head_total += head_left
            head_left = Time.formulateTime(head_left)

            for i in head_motion_right:
                head_right += Time.reverseFormulateTime(i)
            head_total += head_right
            head_right = Time.formulateTime(head_right)

            for i in head_motion_none:
                head_none += Time.reverseFormulateTime(i)
            head_total += head_none
            head_none = Time.formulateTime(head_none)

            head_total = Time.formulateTime(head_total)

            wing_on = 0
            wing_off = 0
            wing_none = 0
            wing_total = 0
            for i in wing_motion_on:
                wing_on += Time.reverseFormulateTime(i)
            wing_total += wing_on
            wing_on = Time.formulateTime(wing_on)

            for i in wing_motion_off:
                wing_off += Time.reverseFormulateTime(i)
            wing_total += wing_off
            wing_off = Time.formulateTime(wing_off)

            for i in wing_motion_none:
                wing_none += Time.reverseFormulateTime(i)
            wing_total += wing_none
            wing_none = Time.formulateTime(wing_none)

            wing_total = Time.formulateTime(wing_total)

            leg_up = 0
            leg_down = 0
            leg_none = 0
            leg_total = 0
            for i in leg_motion_up:
                leg_up += Time.reverseFormulateTime(i)
            leg_total += leg_up
            leg_up = Time.formulateTime(leg_up)

            for i in leg_motion_down:
                leg_down += Time.reverseFormulateTime(i)
            leg_total += leg_down
            leg_down = Time.formulateTime(leg_down)

            for i in leg_motion_none:
                leg_none += Time.reverseFormulateTime(i)
            leg_total += leg_none
            leg_none = Time.formulateTime(leg_none)

            leg_total = Time.formulateTime(leg_total)

            tail_center = 0
            tail_left = 0
            tail_right = 0
            tail_none = 0
            tail_total = 0
            
            
            for i in tail_motion_center:
                tail_center += Time.reverseFormulateTime(i)
            tail_total += tail_center
            tail_center = Time.formulateTime(tail_center)
            
            for i in tail_motion_left:
                tail_left += Time.reverseFormulateTime(i)
            tail_total += tail_left
            tail_left = Time.formulateTime(tail_left)
            
            
            for i in tail_motion_right:
                tail_right += Time.reverseFormulateTime(i)
            tail_total += tail_right
            tail_right = Time.formulateTime(tail_right)

            for i in tail_motion_none:
                tail_none += Time.reverseFormulateTime(i)
            tail_total += tail_none
            tail_none = Time.formulateTime(tail_none)

            tail_total = Time.formulateTime(tail_total)

            data = {
                "Body Part": [
                    "head",
                    "head",
                    "head",
                    "head",
                    "head",
                    "wing",
                    "wing",
                    "wing",
                    "wing",
                    "leg",
                    "leg",
                    "leg",
                    "leg",
                    "tail",
                    "tail",
                    "tail",
                    "tail",
                    "tail",
                ],
                "Status": [
                    "center",
                    "left",
                    "right",
                    "none",
                    "total",
                    "on",
                    "off",
                    "none",
                    "total",
                    "down",
                    "up",
                    "none",
                    "total",
                    "center",
                    "left",
                    "right",
                    "none",
                    "total",
                ],
                "Total Time": [
                    head_center,
                    head_left,
                    head_right,
                    head_none,
                    head_total,
                    wing_on,
                    wing_off,
                    wing_none,
                    wing_total,
                    leg_down,
                    leg_up,
                    leg_none,
                    leg_total,
                    tail_center,
                    tail_left,
                    tail_right,
                    tail_none,
                    tail_total,
                ],
            }

            # create data frame
            df = pd.DataFrame(data).set_index("Body Part")

            with pd.ExcelWriter(
                sheetPath, engine="openpyxl", mode="a", if_sheet_exists="overlay"
            ) as writer:
                df.to_excel(writer, sheet_name="Total Time Statistcs")
        except Exception as ex:
            print(str(ex))

    def readuce(self, changeq, sheetPath):
        try:
            while True:
                change = changeq.get()
                # print(change)
                if change == None:
                    break
                if len(change) == 0:
                    print("EcelWriter: There is no motion happend in this chunk !!")
                    return

                export_details = pd.DataFrame(change).set_index("Time")

                export_details.columns = [
                    "No Motion",
                    "No Motion\n Time Span (sec)",
                    "head status",
                    "head movement",
                    "head movement\n time span",
                    "leg status",
                    "leg movement",
                    "leg movement\n  time span",
                    "wing status",
                    "wing movement",
                    "wing movement\n  time span",
                    "tail status",
                    "tail movement",
                    "tail movement\n  time span",
                ]

                if not os.path.exists(self.sheetPath):
                    with pd.ExcelWriter(sheetPath, engine="openpyxl") as writer:
                        export_details.to_excel(writer, sheet_name="Details")
                else:
                    with pd.ExcelWriter(
                        sheetPath,
                        engine="openpyxl",
                        mode="a",
                        if_sheet_exists="overlay",
                    ) as writer:
                        export_details.to_excel(
                            writer,
                            sheet_name="Details",
                            startrow=writer.sheets["Details"].max_row,
                            header=False,
                        )
                self.TotalTimeCalc(change, sheetPath)
                print("EcelWriter: Exporting data done succesfully.")
        except Exception as ex:
            print(ex)

    def MovementCountCalc(self):
        df = pd.read_excel(self.sheetPath, sheet_name="Details")
        parts_list = []
        sum_all_body = 0
        for part in ["head", "leg", "wing", "tail"]:
            counts = df[f"{part} movement"].value_counts()

            body_part = [part] * (counts.size + 1)
            movements = list(counts.keys()) + ["total"]
            sum_part = sum(counts.values)
            sum_all_body += sum_part
            values = list(counts.values) + [sum_part]

            data = zip(body_part, movements, values)
            parts_list += list(data)

        parts_list.append(("all body", "", sum_all_body))

        export_details = pd.DataFrame(
            parts_list, columns=["Body Part", "Movement", "Count"]
        ).set_index("Body Part")

        with pd.ExcelWriter(
            self.sheetPath, engine="openpyxl", mode="a", if_sheet_exists="overlay"
        ) as writer:
            export_details.to_excel(writer, sheet_name="Movements Count")

    def run(self):
        try:
            with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
                executor.submit(self.readuce, self.excelQueue, self.sheetPath)

            self.MovementCountCalc()

        except Exception as ex:
            print(str(Exception))
