from aquacrop import AquaCropModel, Soil, Crop, InitialWaterContent, IrrigationManagement
from aquacrop.utils import prepare_weather, get_filepath

if __name__ == '__main__':
    path = get_filepath('champion_climate.txt')
    wdf = prepare_weather(path)
    print(wdf)

    sim_start = '1982/05/01'
    sim_end = '2018/10/30'

    soil = Soil('SandyLoam')
    crop = Crop('Maize', planting_date='05/01')
    initWC = InitialWaterContent(value=['FC'])

    # define labels to help after
    labels = []

    outputs = []
    irr_mngt = IrrigationManagement(irrigation_method=1, SMT=[15] * 4)  # specify irrigation management
    model = AquaCropModel(sim_start,
                          sim_end,
                          wdf,
                          soil,
                          crop,
                          initial_water_content=initWC,
                          irrigation_management=irr_mngt)  # create model
    model.run_model(till_termination=True)  # run model till the end
    print(model._outputs.final_stats)  # save results
