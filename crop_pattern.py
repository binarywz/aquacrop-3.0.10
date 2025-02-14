from aquacrop import AquaCropModel, Soil, Crop, InitialWaterContent
from aquacrop.utils import prepare_weather, get_filepath
import pandas as pd

if __name__ == '__main__':
    weather = pd.read_excel("weather.xlsx")
    weather.to_csv('aquacrop/data/weather.txt', sep='\t', index=False)
    weather_file_path = get_filepath('weather.txt')
    pattern_data = {}
    for pattern_row in pd.read_excel('plant_pattern.xlsx').values:
        if pattern_row[0] not in pattern_data.keys():
            aux_list = [pattern_row]
            pattern_data[pattern_row[0]] = aux_list
        else:
            pattern_data[pattern_row[0]].append(pattern_row)
    for pattern_key in pattern_data.keys():
        pattern_cycle = {}
        for pattern in pattern_data[pattern_key]:
            if pattern[1] not in pattern_cycle.keys():
                aux_list = [pattern]
                pattern_cycle[pattern[1]] = aux_list
            else:
                pattern_cycle[pattern[1]].append(pattern)
        pattern_data[pattern_key] = pattern_cycle
    print(pattern_data)
    crop_growth = None
    final_output = None
    water_contents = None
    water_fluxes = None
    pattern_results = None
    for pattern_key in pattern_data.keys():
        pattern = pattern_data[pattern_key]
        sim_yield = 0.0
        for cycle_key in pattern.keys():
            for cycle in pattern[cycle_key]:
                print(cycle)
                model_os = AquaCropModel(
                    sim_start_time=cycle[4],
                    sim_end_time=cycle[5],
                    weather_df=prepare_weather(weather_file_path),
                    soil=Soil(soil_type=cycle[3]),
                    crop=Crop(cycle[2], planting_date=cycle[6]),
                    initial_water_content=InitialWaterContent(value=['FC']),
                )
                model_os.run_model(till_termination=True)
                plant_pattern = str(cycle[0]) + "-" + str(cycle[1]) + "-" + str(cycle[2])
                model_results = model_os.get_simulation_results()
                sim_yield += model_results.values[0][-3] * cycle[-2]
                model_results["pattern"] = [plant_pattern] * model_results.values.shape[0]
                growth_data = model_os.get_crop_growth()
                growth_data["pattern"] = [plant_pattern] * growth_data.values.shape[0]
                water_contents_data = model_os.get_water_storage()
                water_contents_data["pattern"] = [plant_pattern] * water_contents_data.values.shape[0]
                water_fluxes_data = model_os.get_water_flux()
                water_fluxes_data["pattern"] = [plant_pattern] * water_fluxes_data.values.shape[0]
                if crop_growth is None:
                    crop_growth = growth_data
                    final_output = model_results
                    water_contents = water_contents_data
                    water_fluxes = water_fluxes_data
                else:
                    crop_growth = pd.concat([crop_growth, growth_data], ignore_index=True)
                    final_output = pd.concat([final_output, model_results], ignore_index=True)
                    water_contents = pd.concat([water_contents, water_contents_data], ignore_index=True)
                    water_fluxes = pd.concat([water_fluxes, water_fluxes_data], ignore_index=True)
                print(model_results)
        aux_sim_result = pd.DataFrame({'种植制度': [pattern_key], '产量（tonne/ha）': [sim_yield]})
        if pattern_results is None:
            pattern_results = aux_sim_result
        else:
            pattern_results = pd.concat([pattern_results, aux_sim_result], ignore_index=True)


    # 使用ExcelWriter
    with pd.ExcelWriter("pattern_simulation.xlsx", engine='xlsxwriter') as writer:
        pattern_results.to_excel(writer, sheet_name='pattern_sim', index=False)
        final_output.to_excel(writer, sheet_name='model_results', index=False)
        crop_growth.to_excel(writer, sheet_name='crop_growth', index=False)
        water_contents.to_excel(writer, sheet_name='water_contents', index=False)
        water_fluxes.to_excel(writer, sheet_name='water_fluxes', index=False)