# import tb_conexion
import json
from datetime import datetime

from odoo import models


class SyncApi(models.Model):
    _name = "sync.api"

    def sync_api(self, id_product=None, model=None):
        error_data = ""
        model_1 = self.env[model].browse(id_product)
        if model_1.turbodega_type_entity == "turbodega":
            tb_data = model_1.to_json_turbodega()
            log_data = {
                "name": "sync",
                "model_type": model,
                "type_operation": "POST",
                "json_in": json.dumps(tb_data, indent=4, sort_keys=True),
                "stages_id": "new",
            }
            event_obj = self.env["logs.request"].sudo().create(log_data)
            return_value, json_message, url_endpoint = model_1.api_send(tb_data)
            error_data = ""
            if return_value:
                model_1.turbodega_sync = True
                model_1.turbodega_creation = True
                model_1.turbodega_sync_date = datetime.now()
                # model_1.resultado = "envío correcto"
                transaccion_status = "done"
                json_message = json.loads(json_message)
            else:
                transaccion_status = "error"
                # json_message =json.loads(json_message)
                error_data = json_message["faultcode"]
            # print("json_message", json_message)
            event_obj.update(
                {
                    "json_out": json.dumps(json_message, indent=4, sort_keys=True),
                    "error_details": error_data,
                    "stages_id": transaccion_status,
                    "endpoint": url_endpoint,
                }
            )

    def sync_update(self, id_product=None, model=None):
        error_data = ""
        model_1 = self.env[model].browse(id_product)
        if model_1.turbodega_type_entity == "turbodega":
            if model_1.turbodega_creation:
                tb_data = model_1.to_json_turbodega()
                log_data = {
                    "name": "sync",
                    "model_type": model,
                    "type_operation": "PUT",
                    "json_in": json.dumps(tb_data, indent=4, sort_keys=True),
                    "stages_id": "new",
                }
                event_obj = self.env["logs.request"].sudo().create(log_data)
                return_value, json_message, url_endpoint = model_1.api_update_product(
                    tb_data
                )
                # json_message =json.loads(json_message)
                error_data = ""
                if return_value:
                    model_1.turbodega_sync = True
                    model_1.turbodega_sync_date = datetime.now()
                    transaccion_status = "done"

                else:
                    transaccion_status = "error"
                    error_data = json_message["faultcode"]
                event_obj.update(
                    {
                        "json_out": json.dumps(json_message, indent=4, sort_keys=True),
                        "error_details": error_data,
                        "stages_id": transaccion_status,
                        "endpoint": url_endpoint,
                    }
                )
